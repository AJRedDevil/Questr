

import logging as log
import pytz
from decimal import Decimal
from datetime import datetime, time

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
        self.is_weekend = False if self.__current_datetime.weekday() in range(1,6) else True
        log.warn("is it weekend?")
        log.warn(self.is_weekend)
        # self.is_weekend = True
        # 
        self.__rate_meter_drop_weekend = dict(backpack=6, car=8, minivan=10, truck=90)
        self.__rate_per_km_weekend = dict(backpack=1.0, car=1.20, minivan=2.2, truck=90)
        self.__rate_meter_drop_weekday = dict(backpack=5, car=6, minivan=10, truck=90)
        self.__rate_per_km_weekday = dict(backpack=0.8, car=1.0, minivan=2.0, truck=75)
        self.__hourlist = dict(off_peak_hours={'start_hr': 8, 'start_min':00, 'end_hr':21,'end_min':59})
        
        ## Test Data ##
        self.data = {
                'distance' : '5.2',
                'mode' : 'backpack',
                'time_hr' : 22,
                'time_min': 22
        }

        self.peak_hours = self.is_peak_hour()
        log.warn("is it peak_hours?")
        log.warn(self.peak_hours)

    def is_peak_hour(self):
        cur_time = time(self.data['time_hr'], self.data['time_min'])
        start_time = time(self.__hourlist['off_peak_hours']['start_hr'],self.__hourlist['off_peak_hours']['start_min'])
        end_time = time(self.__hourlist['off_peak_hours']['end_hr'],self.__hourlist['off_peak_hours']['end_min'])
        if cur_time >= start_time and cur_time <= end_time:
            return False
        else:
            return True

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
        else:
            return self.__rate_meter_drop_weekday[mode]

    def __get_rate_per_km(self, mode):
        if self.is_weekend or self.peak_hours:
            return self.__rate_per_km_weekend[mode]
        else:
            return self.__rate_per_km_weekday[mode]

    def tests_starting_price(self):
        ## Test Data ##
        self.data = {
                'distance' : '2',
                'mode' : 'backpack',
                'time_hr' : 22,
                'time_min': 22
        }
        self.is_weekend = False
        self.peak_hours = False
        data = self.data
        expected_value = 5.0
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']
        price = float(Decimal(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode)).quantize(Decimal('0.01')))
        self.assertEqual(price, expected_value)


    def tests_is_price_for_weekend(self):
        """Testing if price is true for weekend"""
        self.is_weekend = True
        expected_value = 10.0 # Price
        data = self.data
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']
        price = float(Decimal(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode)).quantize(Decimal('0.01')))
        self.assertEqual(price, expected_value)

    def tests_is_price_for_weekday(self):
        """Testing if price is true for weekday"""
        self.is_weekend = False
        self.peak_hours = False
        expected_value = 8.0 # Price
        data = self.data
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']
        price = float(Decimal(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode)).quantize(Decimal('0.01')))
        self.assertEqual(price, expected_value)

    def tests_is_price_for_peak_hours(self):
        """Testing if price is true for peak hours"""
        self.peak_hours = True
        expected_value = 10.0 # Price
        data = self.data
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']
        price = float(Decimal(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode)).quantize(Decimal('0.01')))
        self.assertEqual(price, expected_value)    

    def get_price(self, data):
        data = self.data
        self.__distance = (float(data['distance']) - 2) if float(data['distance']) > 2 else 0
        self.__shipment_mode = data['mode']

        if self.is_weekend or self.peak_hours:
            return float(Decimal(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode))).quantize(Decimal('0.01'))
        else:
            return float(Decimal(self.__get_meter_drop(self.__shipment_mode) + self.__distance * self.__get_rate_per_km(self.__shipment_mode))).quantize(Decimal('0.01'))

    def tests_if_hour_in_peak_hours(self):
        self.assertEqual(self.peak_hours, True)

