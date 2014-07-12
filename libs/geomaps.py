


import logging as log
import simplejson, urllib
from django.conf import settings
from pprint import pprint


class GMaps(object):
	"""Google Maps Distance API.
	"""
	def __init__(self):
		self.__BASE_URL = "https://maps.googleapis.com/maps/api/directions/json"
		key = getattr(settings, 'GOOGLE_MAPS_SERVER_KEY', None)
		self.__geo_args = {'key':key, 'mode':'driving'}
		self.__result = {}
		self.__status = False

	def set_geo_args(self, geo_args):
		"""Sets the required field-value args
			origin : address upto city
			destination : address upto city
			region : country/area specific 
			units : metric | imperial
			avoid : highways |tolls | ferries
		"""
		self.__geo_args.update(geo_args)

	def __get_directions(self):
		url = self.__BASE_URL + '?' + urllib.urlencode(self.__geo_args)
		log.debug(url)
		self.__result = simplejson.load(urllib.urlopen(url))
		if self.__result:
			self.__status = True if self.__result['status'] == 'OK' else False
			# if self.__status:
			# 	pprint(self.__result['routes'])
		else:
			print 'Error'

	def get_total_distance(self):
		self.__get_directions()
		__distance = 0
		if self.__status:
			for route in self.__result['routes']:
				for leg in route['legs']:
					__distance =  int(leg['distance']['value'])/1000.0
		return __distance


if __name__ == "__main__":
	gmaps = GMaps()
	options = dict(
					avoid='', # highways | tolls | ferries
					units='metric', # metric | imperial
					region='',
					origin='Montreal',
					destination='Toronto'
				)
	geo_args={}
	for field in ['avoid', 'units', 'region', 'origin', 'destination']:
		if options[field]:
			geo_args.update({field:options[field]})
	gmaps.set_geo_args(geo_args)
	distance = gmaps.get_total_distance()
	print distance
