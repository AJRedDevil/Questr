from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext, loader
from models import Contact
import mailchimp
import os

API_KEY = os.environ['MAILCHIMP_API_KEY']
LIST_ID = os.environ['MAILCHIMP_BETA_INVITATION_LIST_ID']

def index(request):
    return render(request, 'beta/index.html')

def thankyou(request):
    return render(request, 'beta/thankyou.html')

def join(request):
	m = mailchimp.Mailchimp(API_KEY)
	email = request.POST['EMAIL']
	new_user = Contact( email = email)
	new_user.save()
	try:
		m.lists.subscribe(LIST_ID, {"email":email})
		m.helper.ping()
	except mailchimp.Error:

		messages.error(request,  "Invalid API key")
	#return HttpResponseRedirect(reverse('beta:thankyou'))
	return render(request, 'beta/thankyou.html', locals())