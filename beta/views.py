from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.contrib import messages
# from django.template import RequestContext, loader


import mailchimp
import logging as log
# from models import Contact
from libs import mailchimp_handler, validations, email_notifier

def index(request):
	messageResponse = "Canada's first<br>peer-to-peer courier.<br>Coming soon."
	return render(request, 'beta/index.html', locals())

def about(request):
	messageResponse = "Canada's first<br>peer-to-peer courier.<br>Coming soon."
	return render(request, 'beta/about.html', locals())

def thankyou(request):
	messageResponse = "Thanks for joining us.<br>Please check your mailbox.</b>"
	return render(request, 'beta/thankyou.html', locals())

# function to join the invitee's subscription list

def join(request):
	if request.method=="POST":
		email = request.POST['EMAIL']
		if email:
			if validations.is_valid_email(email):
				try:
					mailchimp_handler.ping()										
					response = mailchimp_handler.subscribe(email)
					if not response:
						messageResponse = "You have already been subscribed!"
						return render(request, 'beta/index.html', locals())

					messageResponse = "Thanks for joining us.<br>Please check your mailbox.</b>"
					return render(request, 'beta/thankyou.html', locals())
				except mailchimp.Error, e:
					# Error for 
					log.debug(str(e))
					messageResponse = "Something went wrong! We're looking onto it!"
					return render(request, 'beta/index.html', locals())
			else:
				messageResponse="Please provide us with a valid email address!"
				return render(request, 'beta/index.html', locals())
	else:
		messageResponse = "Please enter an email address!"
		return render(request, 'beta/index.html', locals())

def prepNewQuestNotification(name, user_email, message):
    """Prepare the details for notification emails for new quests"""
    template_name="Contact_Us_Notification"
    subject="Hi from a to be Questr!"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'name'   : name,
                                                'email'	: user_email,
                                                'message' : message,
                                                'company'           : "Questr Co"

                                                },
                    }
    return email_details

def contactus(request):
	user_email = request.POST['email']
	name = request.POST['name']
	message = request.POST['message']
	if request.method=="POST":
		if user_email:
			if validations.is_valid_email(user_email):
				try:
					email_details = prepNewQuestNotification(name, user_email, message)
					log.warn(email_details)
					email_notifier.send_contactus_message(email_details)				
					return redirect('index')
				except mailchimp.Error, e:
					# Error for 
					log.debug(str(e))
					messageResponse = "Something went wrong! We're looking onto it!"
					return render(request, 'beta/index.html', locals())
			else:
				messageResponse="Please provide us with a valid email address!"
				return render(request, 'beta/index.html', locals())
	else:
		messageResponse = "Please enter an email address!"
		return redirect('index')
