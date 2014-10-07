

from celery.utils.log import get_task_logger
from questr.celery import app 
 
from quests.models import QuestTransactional
from quests.contrib import quest_handler

import logging

logger = get_task_logger(__name__)

# A periodic task that will run every minute (the symbol "*" means every)
@app.task
def inform_shipper_task(quest_id, courier_id):
    from users.contrib import user_handler
    from users.tasks import activate_shipper
    quest = quest_handler.getQuestDetails(int(quest_id))
    courier = user_handler.getQuestrDetails(int(courier_id))
    accept_transaction = QuestTransactional.objects.get(quest_id=int(quest_id), shipper_id=int(courier_id), transaction_type=1, status=False)
    reject_transaction = QuestTransactional.objects.get(quest_id=int(quest_id), shipper_id=int(courier_id), transaction_type=0, status=False)
    if accept_transaction and reject_transaction:
        reject_transaction.status = True
        accept_transaction.status = True
        # For the shipper didn't respond we put him on hold for 1 hour
        activate_shipper.apply_async((courier_id,), countdown=3600)
        available_couriers = quest.available_couriers
        if len(available_couriers) > 0:
            logging.warn(available_couriers)
            available_couriers.pop(str(courier.id), None)
            quest.available_couriers = available_couriers
            ##Save all the details
            quest.save()
            accept_transaction.save()
            reject_transaction.save()
            couriermanager = user_handler.CourierManager()
            ##Re-run the shipper selection algorithm
            quest = quest_handler.getQuestDetails(int(quest_id))
            couriermanager.informShippers(quest)
