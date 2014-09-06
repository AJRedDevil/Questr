


import Image
import logging as log
import simplejson
import urllib
from cStringIO import StringIO
from django.conf import settings
from pprint import pprint


class GMaps(object):
	"""Google Maps Distance API.
	"""
	def __init__(self):
		self.__BASE_URL = "https://maps.googleapis.com/maps/api/directions/json"
		serverkey = getattr(settings, 'GOOGLE_MAPS_SERVER_KEY', None)
		self.__geo_args = {'key':serverkey, 'mode':'driving'}
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
		log.warn(url)
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
					__distance =  round(int(leg['distance']['value'])/1000.0, 2)
		return __distance


	def __obtain_center_location(self, bounds):
		"""Obtain the center co-ordinates of the map
		"""
		northeast=bounds.get('northeast')
		southwest=bounds.get('southwest')
		lat = (max(northeast['lat'], southwest['lat']) + min(northeast['lat'], southwest['lat']))/2
		lng = (max(northeast['lng'], southwest['lng']) + min(northeast['lng'], southwest['lng']))/2
		center = "{0},{1}".format(lat, lng)
		return center

	def __obtain_static_image_url(self, center, start_location, end_location):
		browserkey = getattr(settings, 'GOOGLE_MAPS_BROWSER_KEY', None)
		# zoom=10
		size="640x640"
		maptype="roadmap"
		url="http://maps.googleapis.com/maps/api/staticmap?center={0}&size={1}&maptype={2}&markers=color:blue|{3}&markers=color:purple|{4}&key={5}".format(center, size, maptype, start_location, end_location, browserkey)
		return url

	# def __save_image(self, bounds, start_location, end_location, filename):
	# 	"""Save the image
	# 	"""
	# 	url = self.__obtain_static_image_url(self.__obtain_center_location(bounds), start_location, end_location)
	# 	with open(filename, 'wb') as f:
	# 		buffer = StringIO(urllib.urlopen(url).read())
	# 		# f.write(urllib.urlopen(url).read())
	# 		image = Image.open(buffer)
	# 		image.save(f, "png")
	# 		# image.show()


	def fetch_static_map(self):
		if self.__status:
			for route in self.__result['routes']:
				bounds = route['bounds']
				for leg in route['legs']:
					start_location = leg['start_location']
					start_location = "{0},{1}".format(start_location['lat'], start_location['lng'])
					end_location = leg['end_location']
					end_location = "{0},{1}".format(end_location['lat'], end_location['lng'])
					map_url = self.__obtain_static_image_url(self.__obtain_center_location(bounds), start_location, end_location)
					return map_url
					# self.__save_image(bounds, start_location, end_location, filename)


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
	gmaps.get_maps() # fetch the static map
