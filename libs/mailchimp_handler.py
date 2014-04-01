

import logging as log
import mailchimp
import os

API_KEY = os.environ['MAILCHIMP_API_KEY']
LIST_ID = os.environ['MAILCHIMP_BETA_INVITATION_LIST_ID']

def __get_mailchimp_api():
	return mailchimp.Mailchimp(API_KEY)

def subscribe(email):
	"""Return True if there is not duplicate email else False
	"""
	m = __get_mailchimp_api()
	try:
		m.lists.subscribe(LIST_ID, {"email":email})
		return True
	except mailchimp.ListAlreadySubscribedError, e:
		log.debug(str(e))
		return False

def ping():
	m = __get_mailchimp_api()
	return m.helper.ping()