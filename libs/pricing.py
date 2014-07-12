

import datetime
import logging as log
import math
from django.utils import timezone


"""
First revision
This revision is intended to serve Questr only when there is no mobile app to determine the available-online shipper ratio.

Weekdays
Off-peak hours        
floor( 4 + SIZE_HANDLING_FEE + (DISTANCE_IN_KM - 2) * 1.7 * SIZE_MODIFIER)
Peak hours            
floor( 4 + SIZE_HANDLING_FEE + (DISTANCE_IN_KM - 2) * 2.2 * SIZE_MODIFIER)    
Low hours        
floor( 6 + SIZE_HANDLING_FEE + (DISTANCE_IN_KM - 2) * 2.5 * SIZE_MODIFIER) 

Weekend
Normal, Peak hours    
floor( 6 + SIZE_HANDLING_FEE + (DISTANCE_IN_KM - 2) * 2.5 * SIZE_MODIFIER)
Low hours        
floor(10 + SIZE_HANDLING_FEE + (DISTANCE_IN_KM - 2) * 3.0 * SIZE_MODIFIER)



SIZE_MODIFIER
Backpack    1.0
Car        1.2
Minivan    2.0

SIZE_HANDLING_FEE
    Backpack      2
    Car          3
    Minivan    12

Off-peak hours
1100-1400, 2000-2300

Peak hours
0800-1000, 1500-1900

Low hours
0000-0700

"""

class WebPricing(object):
	"""Handles the web pricing.
	"""
	def __init__(self):
		# self.__total_time = total_time # total_time
		self.__current_datetime = timezone.now()
		# self.__future_datetime = self.__get_future_datetime()
		# self.__tomorrow = self.__get_tomorrow_datetime()
		

	def set_factors(self, distance, mode='backpack'):
		self.__size_handling_fee = self.__get_size_handling_fee()[mode]
		self.__size_modifier = self.__get_size_modifier()[mode]
		self.__distance = (distance - 2) if distance > 2 else 0
		log.warn("Size Handling fee : %f" % self.__size_handling_fee)
		log.warn("Size modifier : %f" % self.__size_modifier)
		log.warn("Distance : %f" % self.__distance)


	# def __get_future_datetime(self):
	# 	return self.__current_datetime + datetime.timedelta(hours=self.__total_time['hours'], minutes=self.__total_time['minutes'])

	# def __get_tomorrow_datetime(self):
	# 	today = datetime.date.today()
	# 	return today + datetime.timedelta(days=1)

	def __get_size_modifier(self):
		return dict(backpack=1.0, car=1.2, minivan=2.0)

	def __get_size_handling_fee(self):
		return dict(backpack=2, car=3, minivan=12)

	def __hourly_modifier(self):
		return dict(off_peak_hours=range(11,15)+range(20,24), peak_hours=range(8,12)+range(15,20),low_hours=range(0,8))

	def __working_hours(self):
		days = self.__future_datetime.days
		seconds = datetime.timedelta(self.__future_datetime.seconds)
		hours, minutes = tuple(str(seconds).split(":")[:-1])
		return days, hours

	def __get_off_peak_price(self, is_weekend=False):
		if is_weekend:
			return math.floor( 6 + self.__size_handling_fee + self.__distance * 2.5 * self.__size_modifier)
		else:
			return math.floor( 4 + self.__size_handling_fee + self.__distance * 1.7 * self.__size_modifier)

	def __get_peak_hours_price(self, is_weekend=False):
		if is_weekend:
			return math.floor( 6 + self.__size_handling_fee + self.__distance * 2.5 * self.__size_modifier)
		else:
			return math.floor( 4 + self.__size_handling_fee + self.__distance * 2.2 * self.__size_modifier)

	def __get_low_hours_price(self, is_weekend=False):
		if is_weekend:
			return math.floor( 10 + self.__size_handling_fee + self.__distance * 3.0 * self.__size_modifier)
		else:
			return math.floor( 6 + self.__size_handling_fee + self.__distance * 2.5 * self.__size_modifier)

	def __get_weekend_price(self):
		return math.floor( 6 + self.__size_handling_fee + self.__distance * 2.5 * self.__size_modifier)

	def __get_weekday_price(self):
		return math.floor( 4 + self.__size_handling_fee + self.__distance * 1.7 * self.__size_modifier)

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

	def get_price(self):
		"""Returns the price according to the distance set
		"""
		is_weekend = True if self.__current_datetime.weekday() <=5 else False
		if is_weekend:
			return self.__get_weekend_price()
		else:
			return self.__get_weekday_price()

if __name__ == "__main__":
	webpricing = WebPricing()
	webpricing.set_factors(11.7)
	print webpricing.get_price()