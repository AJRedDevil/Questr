

from django.conf import settings

from twilio.rest import TwilioRestClient

class twclient(object):
    """Twilio API Client"""
    def __init__(self):
        self.__twclient = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILO_AUTH_TOKEN)

    def load_newquest_notif(self, quest, accept_url, reject_url):
        msg = ("Pkg {0} nearby, ${1} for {2}km(s). Please respond within 3 minutes, Accept: {3} \
            Decline: {4}" )\
        .format(quest.id, quest.reward,\
            quest.distance, accept_url, reject_url)
        return msg

    def load_acceptquest_notif(self, quest):
        msg = ("You got pkg {0}! Pickup: {1},{2},{3}. {4},{5}   Dropoff: {6},{7},{8}. {9},{10}" )\
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