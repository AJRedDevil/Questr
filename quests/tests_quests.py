

import logging


from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.conf import settings

from datetime import timedelta
import pytz

logger = logging.getLogger(__name__)
from quests.models import Quests

class QuestTests(TestCase):
    """Tests For Quests"""

    def setUp(self):
        self.client = Client()
        self.questrs = 1
        self.creation_date = timezone.now()
        self.title = "New Quest"
        self.size = "backpack"
        self.description = "This is for a new test"
        self.srccity = "Toronto"
        self.srcaddress = "Alan Powell Ln"
        self.srcpostalcode = "M5S1K4"
        self.srcname = "Frank Qin"
        self.srcphone = "1234567890"
        self.pickup = dict(city=self.srccity,address=self.srcaddress,postalcode=self.srcpostalcode,
            name=self.srcname,phone=self.srcphone
            )
        self.dstcity = "Markham"
        self.dstaddress = "65 Maria Rd"
        self.dstpostalcode = "L6E2G9"
        self.dstname = "Gaurav Ghimire"
        self.dstphone = "1987654320"
        self.reward = "89"
        self.distance = "19"
        self.tracking_number = "jkalsken2n"
        self.dropoff = dict(city=self.dstcity,address=self.dstaddress,postalcode=self.dstpostalcode,
            name=self.dstname,phone=self.dstphone
            )
        self.data = dict(questrs_id=self.questrs,title=self.title,size=self.size,description=self.description,pickup=self.pickup,
            dropoff=self.dropoff, tracking_number=self.tracking_number)

    def tests_post_new_quest(self):
        questdetails = Quests(questrs_id=self.questrs,title=self.title,size=self.size,description=self.description,pickup=self.pickup,
            dropoff=self.dropoff, reward=self.reward, creation_date = self.creation_date)
        Quests.save(questdetails)
        questdetails = Quests.objects.get(title=self.title)
        self.assertEqual(questdetails.title, "New Quest")


    def tests_tracking_number_search(self):
        questdetails = Quests(questrs_id=self.questrs,title=self.title,size=self.size,description=self.description,pickup=self.pickup,
            dropoff=self.dropoff, reward=self.reward, creation_date = self.creation_date, tracking_number=self.tracking_number)
        Quests.save(questdetails)
        questdetails = Quests.objects.get(title=self.title)
        tracking_number = questdetails.tracking_number
        self.assertEqual(tracking_number, self.tracking_number)
        response = self.client.get('/track/?tracking_number=%s' % tracking_number)
        self.assertEqual(response.status_code, 200)

    def tests_pickup_time(self):
        ##pickup time is after 1 hour##
        self.current_time = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))
        self.pickup_time = self.current_time+timedelta(hours=1)
        questdetails = Quests(questrs_id=self.questrs,title=self.title,size=self.size,description=self.description,pickup=self.pickup,
            dropoff=self.dropoff, reward=self.reward, creation_date = self.creation_date, tracking_number=self.tracking_number, pickup_time=self.pickup_time)
        Quests.save(questdetails)
        questdetails = Quests.objects.get(title=self.title)
        self.assertEqual(questdetails.pickup_time.hour, 12)
