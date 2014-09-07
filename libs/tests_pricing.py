

import logging as log
import pytz
import math

from django.utils import timezone
from django.conf import settings
from django.test.client import Client

from django.test import TestCase

class PricingTestCase(TestCase):
    """docstring for PricingTestCase"""

    distance = -1
    mode='backpack'

    def setUp(self):
        ## Getting the time as per the local timezone
        self.__current_datetime = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))
        ## Check if it's the weekend
        self.is_weekend = True if self.__current_datetime.weekday() <=5 else False
        # self.is_weekend = True
        # 
        self.__rate_meter_drop_weekend = dict(backpack=6, car=8, minivan=10, truck=90)
        self.__rate_per_km_weekend = dict(backpack=1.0, car=1.20, minivan=2.2, truck=90)
        self.__rate_meter_drop_weekday = dict(backpack=4, car=6, minivan=10, truck=90)
        self.__rate_per_km_weekday = dict(backpack=0.8, car=1.0, minivan=2.0, truck=75)
        self.__hourlist = dict(off_peak_hours=range(8,22),peak_hours=range(22,24)+range(0,9))
        
        ## Test Data ##
        self.data = {
                'distance' : '5.2',
                'mode' : 'backpack',
                'hour' : '02'
        }

        self.peak_hours = True if self.data['hour'] in self.__hourlist['peak_hours'] else False


    def tests_get_rate_meter_drop(self, expected_value=6):
        mode = self.data['mode']
        if self.is_weekend or self.peak_hours:
            expected_value=6
            self.rate_meter_drop = self.__rate_meter_drop_weekend[mode]
        else:
            expected_value=4
            self.rate_meter_drop = self.__rate_meter_drop_weekday[mode]
        self.assertEqual(self.rate_meter_drop, expected_value)

    def __get_meter_drop(self, mode):
        mode = self.data['mode']
        if self.is_weekend or self.peak_hours:
            return self.__rate_meter_drop_weekend[mode]
        return self.__rate_meter_drop_weekday[mode]

    def __get_rate_per_km(self, mode):
        if self.is_weekend or self.peak_hours:
            return self.__rate_per_km_weekend[mode]
        return self.__rate_per_km_weekday[mode]

    def tests_is_price_for_weekend(self):
        """Testing if price is true for weekend"""
        self.is_weekend = True
        expected_value = 9.0 # Price
        data = self.data
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']
        price = math.floor(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode))
        self.assertEqual(price, expected_value)

    def tests_is_price_for_weekday(self):
        """Testing if price is true for weekday"""
        self.is_weekend = False
        expected_value = 6.0 # Price
        data = self.data
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']
        price = math.floor(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode))
        self.assertEqual(price, expected_value)

    def tests_is_price_for_peak_hours(self):
        """Testing if price is true for peak hours"""
        self.peak_hours = True
        expected_value = 9.0 # Price
        data = self.data
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']
        price = math.floor(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode))
        self.assertEqual(price, expected_value)    

    def get_price(self, data):
        data = self.data
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']
        self.__hour = self.__current_datetime.hour

        if self.is_weekend or self.peak_hours:
            return round(math.floor(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode)))
        
        return round(math.floor(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode)))

