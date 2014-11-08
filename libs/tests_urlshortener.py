

import logging


from django.test import TestCase

from libs.url_shortener import UrlShortener


logger = logging.getLogger(__name__)

class ShortURLTest(TestCase):
    """Tests For URL Shortener"""
    def setUp(self):
        self.surl = UrlShortener()

    def tests_1_is_None(self):
        long_url = 'http://www.que;0989023ojfalksjf2lkjlkjflsakjfsastr.co'
        post_data = dict(longUrl=long_url)
        shorturl = self.surl.get_short_url(post_data)
        logger.warn(shorturl)
        self.assertEqual(shorturl, None)

    def tests_2_is_not_None(self):
        long_url= 'http://localhost:5000/quest/accept/e3e25e0?quest_token=dcfa53'
        post_data = dict(longUrl=long_url)
        shorturl = self.surl.get_short_url(post_data)
        logger.warn(shorturl)
        self.assertNotEqual(shorturl, None)

    def tests_3_url_if_None(self):
        accept_link = "http://que   989023ojfalksjf2lkjlkjt/accept/e3e25e0?quest_token=dcfa53"        
        post_data = dict(longUrl=accept_link)
        from libs.url_shortener import UrlShortener
        shortener = UrlShortener()
        short_url = shortener.get_short_url(post_data)
        if short_url==None:
            url=accept_link
        else:
            url=short_url 
        logger.warn(url)
        self.assertEqual(url,accept_link)

    def tests_4_url_if_not_None(self):
        accept_link = "http://localhost:5000/qu;est/accept/e3e25e0?quest_token=dcfa53"        
        post_data = dict(longUrl=accept_link)
        from libs.url_shortener import UrlShortener
        shortener = UrlShortener()
        short_url = shortener.get_short_url(post_data)
        if short_url==None:
            url=accept_link
        url=short_url 
        logger.warn(url)
        self.assertNotEqual(url,accept_link)