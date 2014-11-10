

from django.conf import settings

from twilio.rest import TwilioRestClient
import logging
# Init Logger
logger = logging.getLogger(__name__)

class twclient(object):
    """Twilio API Client"""
    def __init__(self):
        self.__twclient = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILO_AUTH_TOKEN)

    def load_newquest_notif(self, quest, accept_url, reject_url):
        msg = ("New Pkg {0} nearby, ${1} for {2}km(s). Accept: {3} Decline: {4}" )\
        .format(quest.id, quest.reward,\
            quest.distance, accept_url, reject_url)
        #Adding quest message to the detail
        message = quest.description
        charleft = abs(154 - len(msg))
        #truncating message to the amount of chars remaining in the text message
        truncated_message = (message[:charleft] + '..') if len(message) > charleft else message
        msg = msg+' Msg: '+truncated_message
        return msg

    def load_acceptquest_notif(self, quest):
        msg = ("You got pkg {0}! Pickup: {1},{2},{3}. {4},{5}  Dropoff: {6},{7},{8}. {9},{10}" )\
        .format(quest.id, quest.pickup['address'], quest.pickup['city'],\
            quest.pickup['postalcode'], quest.pickup['name'], quest.pickup['phone'], quest.dropoff['address'], quest.dropoff['city'],\
            quest.dropoff['postalcode'], quest.dropoff['name'], quest.dropoff['phone'])
        return msg

    def sendmessage(self, receiver, message):
        num = settings.TWILIO_NUM_1
        try:
            conn = self.__twclient.messages.create(from_=num,body=message,to=receiver)
        except Exception, e:
            raise e
        return conn.sid

    def getclient(self):
        return self.__twclient