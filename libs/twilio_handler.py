

from django.conf import settings

from twilio.rest import TwilioRestClient

class twclient(object):
    """Twilio API Client"""
    def __init__(self):
        self.__twclient = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILO_AUTH_TOKEN)

    def load_newquest_notif(self, accept_url, reject_url):
        msg = ("Accept - {0} ... Reject - {1} --Questr").format(accept_url, reject_url)
        return msg

    def load_acceptquest_notif(self, quest):
        msg = ("Pickup: {0}({1}), {2},{3},{4} ... Dropoff: {5}({6}), {7},{8},{9}" ).format(quest.pickup['name'], quest.pickup['phone'],\
            quest.pickup['address'], quest.pickup['postalcode'], quest.pickup['city'], quest.dropoff['name'], quest.dropoff['phone'],\
            quest.dropoff['address'], quest.dropoff['postalcode'], quest.dropoff['city'])
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