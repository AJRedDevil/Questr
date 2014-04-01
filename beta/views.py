from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.contrib import messages
# from django.template import RequestContext, loader
from models import Contact
from questr.globals import validateEmail

import os, mailchimp

API_KEY = os.environ['MAILCHIMP_API_KEY']
LIST_ID = os.environ['MAILCHIMP_BETA_INVITATION_LIST_ID']

def index(request):
    return render(request, 'beta/index.html')

# def thankyou(request):
# 	messageResponse = "Thanks for joining us.<br>Please check your mailbox.</b>"
# 	return render(request, 'beta/thankyou.html', locals())

# function to join the invitee's subscription list
def join(request):
	mcObject = mailchimp.Mailchimp(API_KEY)
	email = request.POST['EMAIL']
	isCorrect = validateEmail(email)
	if not isCorrect:
		messageResponse="Please provide with a valid email address!"
		return render(request, 'beta/thankyou.html', locals())
	new_user = Contact( email = email)
	new_user.save()
	try:
		mcObject.lists.subscribe(LIST_ID, {"email":email})
		mcObject.helper.ping()
	except mailchimp.Error:
		messages.error(request,  "Invalid API key")
	messageResponse = "Thanks for joining us.<br>Please check your mailbox.</b>"
	# return HttpResponseRedirect(reverse('beta:thankyou'))	
	return render(request, 'beta/thankyou.html', locals())

