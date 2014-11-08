

#All Django Imports
from django.conf import settings

#All external imports (libs, packages)
import logging as log
import simplejson
import urllib
import urllib2


class UrlShortener(object):
    """
    Google URL Shortener API.
    """
    def __init__(self):
        self.__BASE_URL = "https://www.googleapis.com/urlshortener/v1/url"
        serverkey = getattr(settings, 'GOOGLE_SERVER_API_KEY', None)
        self.__args = {'key':serverkey}
        self.__result = {}
        self.__status = False

    def set_args(self, args):
        self.__args.update(args)

    def __get_url(self, data):
        # log.warn(data)
        headers = {'Content-Type': 'application/json'}
        url = self.__BASE_URL + '?' + urllib.urlencode(self.__args)
        # log.warn(url)
        req = urllib2.Request(url, simplejson.dumps(data), headers)
        # log.warn(url)

        try:
            self.__result = simplejson.load(urllib2.urlopen(req))
            return True
        except Exception, e :
            log.warn(e)
            return False

    def get_short_url(self, data):
        status = self.__get_url(data)
        __url = None
        if status:
            __url =  self.__result['id']
        return __url
