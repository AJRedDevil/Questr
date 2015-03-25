import os
import requests
import logging
# Init Logger
logger = logging.getLogger(__name__)


class OnboardIQConnector(object):
    """
    Onobard IQ Connector and handler for applications
    """
    def __init__(self):
        self.__outgoingurl = 'https://www.onboardiq.com/api/v1/applicants'
        # self.__apikey = os.environ['ONBOARDIQ_API_KEY']

    def sendApplicationDetail(self, data):
        data = data.dict()
        try:
            req = requests.post(self.__outgoingurl, data, verify=False)
            if req.status_code == 200:
                logger.warn('done')
        except Exception, e:
            logger.warn(e)
