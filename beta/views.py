from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext, loader
from models import Contact
import mailchimp

API_KEY = "0bcdb957ee18611ed49045a5a1df196d-us8"
LIST_ID = "7f3d74a524"

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