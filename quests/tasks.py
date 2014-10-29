

from celery.utils.log import get_task_logger
from questr.celery import app 
 
from quests.models import QuestTransactional
from quests.contrib import quest_handler

from django.conf import settings

import logging

logger = get_task_logger(__name__)

@app.task
def inform_shipper_task(quest_id, courier_id):
    from users.contrib import user_handler
    from users.tasks import activate_shipper
    quest = quest_handler.getQuestDetails(int(quest_id))
    courier = user_handler.getQuestrDetails(int(courier_id))

    try:
        accept_transaction = QuestTransactional.objects.get(quest_id=int(quest_id), shipper_id=int(courier_id), transaction_type=1, status=False)
    except Exception, e:
        logger.warn(e)
        accept_transaction = False

    try:
        reject_transaction = QuestTransactional.objects.get(quest_id=int(quest_id), shipper_id=int(courier_id), transaction_type=0, status=False)
    except Exception, e:
        logger.warn(e)
        reject_transaction = False

    if accept_transaction and reject_transaction:
        reject_transaction.status = True
        accept_transaction.status = True
        # For the shipper didn't respond we put him on hold for 1 hour
        activate_shipper.apply_async((courier_id,), countdown=int(settings.COURIER_ACTIVATION_INTERVAL))
        eventmanager = quest_handler.QuestEventManager()
        extrainfo = dict(detail="No response from courier", selected_courier=courier_id)
        eventmanager.setevent(quest, 6, extrainfo)
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
    
    # if quest.shipper == None:
    #     available_couriers = quest.available_couriers
    #     if len(available_couriers) > 0:
    #         logging.warn(available_couriers)
    #         available_couriers.pop(str(courier.id), None)
    #         quest.available_couriers = available_couriers
    #         ##Save all the details
    #         quest.save()
    #     couriermanager = user_handler.CourierManager()
    #     couriermanager.informShippers(quest)

@app.task
def init_courier_selection(quest_id):
    message = "Inititating selection for quest {0}".format(quest_id)
    logger.debug(message)
    from users.contrib import user_handler
    from quests.contrib import quest_handler
    couriermanager = user_handler.CourierManager()
    questdata = quest_handler.getQuestDetails(quest_id)
    extrainfo = dict(detail="Courier selection started")
    eventmanager = quest_handler.QuestEventManager()
    eventmanager.setevent(questdata, 2, extrainfo)
    couriermanager.informShippers(questdata)

@app.task
def checkstatus():
    message = "Checking status"
    logger.debug(message)
    return True