from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.contrib import messages
# from django.template import RequestContext, loader


import mailchimp
import logging as log
from models import Contact
from libs import mailchimp_handler, validations

def index(request):
    return render(request, 'beta/index.html')

# def thankyou(request):
# 	messageResponse = "Thanks for joining us.<br>Please check your mailbox.</b>"
# 	return render(request, 'beta/thankyou.html', locals())

# function to join the invitee's subscription list

def join(request):
	email = request.POST['EMAIL']
	if email:
		if validations.is_valid_email(email):
			try:
				response = mailchimp_handler.subscribe(email)
				if not response:
					messageResponse = "You have already been subscribed"
					return render(request, 'beta/index.html', locals())
				else:
					mailchimp_handler.ping()
					
					new_user = Contact( email = email)
					new_user.save()
					
					messageResponse = "Thanks for joining us.<br>Please check your mailbox.</b>"
					# return HttpResponseRedirect(reverse('beta:thankyou'))	
					return render(request, 'beta/thankyou.html', locals())
			except mailchimp.Error, e:
				# Error for 
				log.debug(str(e))
				messageResponse = "Something went wrong"
				return render(request, 'beta/thankyou.html', locals())
		else:
			messageResponse="Please provide with a valid email address!"
			return render(request, 'beta/thankyou.html', locals())
	else:
		messageResponse = "Please enter the email address"
		return render(request, 'beta/index.html', locals())

