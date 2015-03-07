from django.shortcuts import render, redirect
# from django.conf import settings
# from social.backends.google import GooglePlusAuth ###disabled google plus##
# from django.template import RequestContext, loader

import mailchimp
import logging
# Init Logger
logger = logging.getLogger(__name__)
# from models import Contact
from libs import mailchimp_handler, validations, email_notifier


def index(request):
    if request.user.is_authenticated():
        return redirect('home')
    # plus_id = getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None) ###disabled google plus##
    # plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE) ###disabled google plus##
    pagetitle = "Deliver anything anytime in minutes"
    return render(request, 'index.html', locals())


def loadPage(request, template):
    user = request.user
    return render(request, template, locals())


def contact(request):
    """Returns the contactus page"""
    user = request.user
    pagetitle = "Contact US"
    return render(request, 'contact.html', locals())


def about(request):
    """Returns the about us page"""
    user = request.user
    pagetitle = "About Us"
    return render(request, 'about.html', locals())


def news(request):
    """Returns the news page"""
    user = request.user
    pagetitle = "In the news !"
    return render(request, 'news.html', locals())


def crowdshipping(request):
    user = request.user
    """Returns the about crowdshipping page"""
    return render(request, 'crowdshipping.html', locals())


def trust(request):
    """Returns the HOW questr is safe page"""
    user = request.user
    pagetitle = "Trust"
    return render(request, 'trust.html', locals())


def terms(request):
    """Returns the TOS"""
    user = request.user
    pagetitle = "Terms of Service"
    return render(request, 'terms.html', locals())


def privacy(request):
    """Returns the Privacy Policy"""
    user = request.user
    pagetitle = "Privacy Policy"
    return render(request, 'privacy.html', locals())


def faq(request):
    user = request.user
    pagetitle = "Frequently Asked Questions"
    return render(request, 'faq.html', locals())


def thankyou(request):
    messageResponse = "Thanks for joining us.<br>Please check your mailbox.</b>"
    pagetitle = "Thanks for joining us !"
    return render(request, 'thankyou.html', locals())

# function to join the invitee's subscription list


def join(request):
    """Subscribe to the mailing list"""
    if request.POST:
        logger.debug(request.POST)
        email = request.POST['EMAIL']
        if email:
            if validations.is_valid_email(email):
                try:
                    mailchimp_handler.ping()
                    response = mailchimp_handler.subscribe(email)
                    if not response:
                        # Alert here
                        # messageResponse = "You have already been subscribed with ... "
                        return redirect('index')

                    logger.debug("{0} has been subscribed".format(email))
                    # Alert here
                    # messageResponse = "Thanks for joining us. Please check your email to be a part of ..."
                    return redirect('index')
                except mailchimp.Error, e:
                    logger.debug(str(e))
                    # Alert here
                    # messageResponse = "Something went wrong! We're looking onto it!"
                    return redirect('index')
            else:
                # Alert here
                # messageResponse="Please provide us with a valid email address!"
                return redirect('index')
    else:
        pagetitle = "Join Us"
        return render(request, 'join.html', locals())


def prepContactUsNotification(name, user_email, message):
    """Prepare the details for contact us notifications"""
    template_name = "Contact_Us_Notification"
    subject = user_email+' '+"says hello!"

    email_details = {
        'subject': subject,
        'template_name': template_name,
        'global_merge_vars': {
            'name': name,
            'email': user_email,
            'message': message,
            'company': "Questr Co"
        },
    }
    return email_details


def contactus(request):
    """Contact Us for visitors"""
    user_email = request.POST['email']
    name = request.POST['name']
    message = request.POST['message']
    if request.POST:
        logger.debug(request.POST)
        if user_email:
            if validations.is_valid_email(user_email):
                try:
                    email_details = prepContactUsNotification(
                        name,
                        user_email,
                        message
                    )
                    logger.debug(email_details)
                    email_notifier.send_contactus_notification(
                        'hello@questr.co',
                        email_details
                    )
                    return redirect('index')
                except mailchimp.Error, e:
                    # Alert here
                    logger.debug(str(e))
                    # messageResponse = "Something went wrong! We're looking onto it!"
                    pagetitle = "Contact Us"
                    return redirect('index')
            else:
                # Alert here
                pagetitle = "Contact Us"
                # messageResponse="Please provide us with a valid email address!"
                return redirect('index')
    else:
        # Alert here
        # messageResponse = "Please enter an email address!"
        return redirect('index')
