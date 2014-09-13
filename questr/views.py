from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from social.backends.google import GooglePlusAuth ###disabled google plus##
from django.contrib import messages
# from django.template import RequestContext, loader

import mailchimp
import logging as log
# from models import Contact
from libs import mailchimp_handler, validations, email_notifier

def index(request):
    if request.user.is_authenticated():
        return redirect('home')
    # plus_id = getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None) ###disabled google plus##
    # plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE) ###disabled google plus##
    pagetitle = "Cheaper, faster, 24/7 shipments in GTA"
    return render(request, 'index.html', locals())

def loadPage(request, template):
    return render(request, template, locals())

def contact(request):
    pagetitle = "Contact US"
    return render(request, 'contact.html', locals())

def about(request):
    pagetitle = "About Us"
    return render(request, 'about.html', locals())

def news(request):
    pagetitle = "In the news !"
    return render(request, 'news.html', locals())

def crowdshipping(request):
    return render(request, 'crowdshipping.html', locals())

def trust(request):
    pagetitle = "Trust"
    return render(request, 'trust.html', locals())

def terms(request):
    pagetitle = "Terms of Service"
    return render(request, 'terms.html', locals())

def privacy(request):
    pagetitle = "Privacy Policy"
    return render(request, 'privacy.html', locals())

def faq(request):
    pagetitle = "Frequently Asked Questions"
    return render(request, 'faq.html', locals())

def thankyou(request):
    messageResponse = "Thanks for joining us.<br>Please check your mailbox.</b>"
    pagetitle = "Thanks for joining us !"
    return render(request, 'thankyou.html', locals())

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
                        messageResponse = "You have already been subscribed with ... "
                        return render(request, 'index.html', locals())

                    messageResponse = "Thanks for joining us. Please check your email to be a part of ..."
                    return render(request, 'index.html', locals())
                except mailchimp.Error, e:
                    # Error for 
                    log.debug(str(e))
                    messageResponse = "Something went wrong! We're looking onto it!"
                    return render(request, 'index.html', locals())
            else:
                messageResponse="Please provide us with a valid email address!"
                return render(request, 'index.html', locals())
    else:
        pagetitle = "Join Us"
        return render(request, 'join.html', locals())

def prepContactUsNotification(name, user_email, message):
    """Prepare the details for notification emails for new quests"""
    template_name="Contact_Us_Notification"
    subject=user_email+' '+"says hello!"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'name'   : name,
                                                'email' : user_email,
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
                    email_details = prepContactUsNotification(name, user_email, message)
                    log.warn(email_details)
                    email_notifier.send_contactus_notification(user_email, email_details)             
                    return redirect('index')
                except mailchimp.Error, e:
                    # Error for 
                    log.debug(str(e))
                    messageResponse = "Something went wrong! We're looking onto it!"
                    pagetitle = "Contact Us"
                    return render(request, 'index.html', locals())
            else:
                pagetitle = "Contact Us"
                messageResponse="Please provide us with a valid email address!"
                return render(request, 'index.html', locals())
    else:
        messageResponse = "Please enter an email address!"
        return redirect('index')