from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext, loader
from beta.models import Contact
import mailchimp

def index(request):
    return render(request, 'beta/index.html')
	
def join(request):
	m = mailchimp.Mailchimp('as44521cd4e74f54005bdff4ff7bf98e52-us8')
	new_user = Contact( email = request.POST['email'])
	new_user.save()
	try:
		m.helper.ping()
	except mailchimp.Error:
		messages.error(request,  "Invalid API key")
	#return HttpResponseRedirect(reverse('beta:thankyou'))
	return render_to_response('beta/index.html', {}, context_instance=RequestContext(request))
	