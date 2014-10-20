

import pytz
from decimal import Decimal
import logging as log

from datetime import time

from django.utils import timezone
from django.conf import settings

"""
First revision
This revision is intended to serve Questr only when there is no mobile app to determine the available-online shipper ratio.
float( rate_meter_drop + (distance - 2) * $/km ) 

Weekdays
Off-peak hours        
float( RATE_METER_DROP_WEEKDAY + (DISTANCE_IN_KM - 2) * RATE_PER_METER_WEEKDAY)
Peak hours            
float( RATE_METER_DROP_WEEKDAY + (DISTANCE_IN_KM - 2) * RATE_PER_METER_WEEKEND)    

Weekend
Normal, Peak hours    
float( RATE_METER_DROP_WEEKEND + (DISTANCE_IN_KM - 2) * RATE_PER_METER_WEEKEND)

RATE_METER_DROP_WEEKDAY
Backpack   			4
Car        			6
Minivan    			10
Truck(per hour)		90

RATE_METER_DROP_WEEKEND
Backpack   			6
Car        			8
Minivan    			10
Truck(per hour)		90

RATE_PER_KM_WEEKDAY
Backpack   			0.8
Car        			1.0
Minivan    			2.0
Truck(per hour)		75

RATE_PER_KM_WEEKEND
Backpack   			1.0
Car        			1.20
Minivan    			2.2
Truck(per hour)		90

Off-peak hours
0900-2100

Peak hours
2200-0800

"""

class WebPricing(object):
	"""Handles the web pricing.
	"""
	def __init__(self):
		# self.__total_time = total_time # total_time
		self.__current_datetime = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))
		#self.is_weekend = False if self.__current_datetime.weekday() in range(1,6) else True
		# Removed weekend meter drop
		self.is_weekend = False
		# log.warn("is it weekend?")
		# log.warn(self.is_weekend)
		self.clock_hour = self.__current_datetime.hour
		self.clock_minute = self.__current_datetime.minute
		self.__rate_meter_drop_weekend = dict(backpack=6, car=8, minivan=10, truck=90)
		self.__rate_per_km_weekend = dict(backpack=1.0, car=1.20, minivan=2.2, truck=90)
		self.__rate_meter_drop_weekday = dict(backpack=5, car=6, minivan=10, truck=90)
		self.__rate_per_km_weekday = dict(backpack=0.8, car=1.0, minivan=2.0, truck=75)
		# self.__hourlist = dict(off_peak_hours=range(8,22),peak_hours=range(22,24)+range(0,9))
		self.__hourlist = dict(off_peak_hours={'start_hr': 8, 'start_min':00, 'end_hr':21,'end_min':59})
		# self.peak_hours = True if self.clock_hour in self.__hourlist['peak_hours'] else False
		self.peak_hours = self.__is_peak_hour()
		# log.warn("is it peakhour?")
		# log.warn(self.peak_hours)
		# self.__future_datetime = self.__get_future_datetime()
		# self.__tomorrow = self.__get_tomorrow_datetime()
	
	def __get_meter_drop_rate(self, mode='backpack'):
		if self.is_weekend or self.peak_hours:
		    rate_meter_drop = self.__rate_meter_drop_weekend[mode]
		else:
			rate_meter_drop = self.__rate_meter_drop_weekday[mode]
		return rate_meter_drop

	def __get_rate_per_km(self, mode='backpack'):
		log.warn(self.is_weekend)
		log.warn(self.peak_hours)
		if self.is_weekend or self.peak_hours:
			log.warn("hello")
			rate_per_km = self.__rate_per_km_weekend[mode]
		else:
			rate_per_km = self.__rate_per_km_weekday[mode]
		return rate_per_km

	def __is_peak_hour(self):
		# cur_time = time(self.clock_hour, self.clock_minute)
		# start_time = time(self.__hourlist['off_peak_hours']['start_hr'],self.__hourlist['off_peak_hours']['start_min'])
		# end_time = time(self.__hourlist['off_peak_hours']['end_hr'],self.__hourlist['off_peak_hours']['end_min'])
		# if cur_time >= start_time and cur_time <= end_time:
		# 	return False
		# else:
		# 	return True
		# Removed peak_hour selection for now
		return False
		
	# def set_factors(self, distance, mode='backpack'):
	# 	self.__size_meter_drop = self.__get_size_meter_drop()[mode]
	# 	self.__distance = (distance - 2) if distance > 2 else 0
	# 	log.warn("Size Handling fee : %f" % self.__size_meter_drop)
	# 	log.warn("Size modifier : %f" % self.__size_modifier)
	# 	log.warn("Distance : %f" % self.__distance)

	# def __working_hours(self):
	# 	days = self.__future_datetime.days
	# 	seconds = datetime.timedelta(self.__future_datetime.seconds)
	# 	hours, minutes = tuple(str(seconds).split(":")[:-1])
	# 	return days, hours

	# def __get_off_peak_price(self, is_weekend=False):
	# 	if is_weekend:
	# 		return Decimal( 6 + self.__size_meter_drop + self.__distance * 2.5 * self.__size_modifier).quantize(Decimal('0.01')))
	# 	else:
	# 		return Decimal( 4 + self.__size_meter_drop + self.__distance * 1.7 * self.__size_modifier).quantize(Decimal('0.01')))

	# def __get_peak_hours_price(self, is_weekend=False):
	# 	if is_weekend:
	# 		return Decimal( 6 + self.__size_meter_drop + self.__distance * 2.5 * self.__size_modifier).quantize(Decimal('0.01')))
	# 	else:
	# 		return Decimal( 4 + self.__size_meter_drop + self.__distance * 2.0 * self.__size_modifier).quantize(Decimal('0.01')))

	# def __get_low_hours_price(self, is_weekend=False):
	# 	if is_weekend:
	# 		return Decimal( 10 + self.__size_meter_drop + self.__distance * 3.0 * self.__size_modifier).quantize(Decimal('0.01')))
	# 	else:
	# 		return Decimal(  6 + self.__size_meter_drop + self.__distance * 2.5 * self.__size_modifier).quantize(Decimal('0.01')))

	def __get_weekend_price(self, distance, shipment_mode):
		log.warn(self.__get_rate_per_km(shipment_mode))
		return float(Decimal(self.__get_meter_drop_rate(shipment_mode) + distance * self.__get_rate_per_km(shipment_mode)).quantize(Decimal('0.01')))

	def __get_weekday_price(self, distance, shipment_mode):
		log.warn(self.__get_rate_per_km(shipment_mode))
		return float(Decimal(self.__get_meter_drop_rate(shipment_mode) + distance * self.__get_rate_per_km(shipment_mode)).quantize(Decimal('0.01')))

	# def get_price(self):
	# 	starting_hour = self.__current_datetime.hours
	# 	days, hours = self.__working_hours()
	# 	price = 0.0
	# 	if days < 1:
	# 		is_weekend = True if self.__current_datetime.weekday() <=5 else False
			
	# 	else:
	# 		is_weekend = True if self.__current_datetime.weekday() <=5 else False

	# 	return price

	# 	pass

	def get_price(self, distance, shipment_mode='backpack'):
		"""Checks if it's a peak hour or a weekend, and returns the respective price for the distance"""
		self.__distance = (float(distance) - 2) if float(distance) > 2 else 0
		self.__shipment_mode = shipment_mode
		log.warn(self.peak_hours)
		if self.is_weekend or self.peak_hours:
			# log.warn("Travelling %s km on %s at %s00 hrs, a charge of $%s is incurred" % self.__distance, self.__shipment_mode, self.clock_hour, self.__get_weekend_price(self.__distance, self.__shipment_mode))
			log.warn("Shipping {0} km(s) on {1} at {2}{3} hrs, a charge of {4} is incurred".format(self.__distance, self.__shipment_mode, self.clock_hour, self.clock_minute, self.__get_weekend_price(self.__distance, self.__shipment_mode)))
			return self.__get_weekend_price(self.__distance, self.__shipment_mode)
		else:	    	
			# log.warn("Travelling %s km on %s at %s00 hrs, a charge of $%s is incurred" % self.__distance, self.__shipment_mode, self.clock_hour, self.__get_weekday_price(self.__distance, self.__shipment_mode))
			log.warn("Shipping {0} km(s) on {1} at {2}{3} hrs, a charge of {4} is incurred".format(self.__distance, self.__shipment_mode, self.clock_hour, self.clock_minute ,self.__get_weekday_price(self.__distance, self.__shipment_mode)))
			return self.__get_weekday_price(self.__distance, self.__shipment_mode)


	# def get_price(self):
	# 	"""Returns the price according to the distance set
	# 	"""
	# 	is_weekend = True if self.__current_datetime.weekday() <=5 else False
	# 	if is_weekend:
	# 		return self.__get_weekend_price()
	# 	else:
	# 		return self.__get_weekday_price()

if __name__ == "__main__":
	webpricing = WebPricing()
	print webpricing.get_price(60)
