

import logging
from django.core.mail import EmailMessage


def __get_verification_template(template_name, first_name, email, verf_link):
    """
    Returns the template for email verification.
    """
    ##Email Template Init###
    email_template = EmailMessage(
        subject="Please verify your email!",
        from_email="Questr <hello@questr.co>",
        to=[email],
        headers={'Reply-To': "Questr <hello@questr.co>"}
        )

    ###List Email Template###
    email_template.template_name = template_name

    ###List Email Tags to be used###
    email_template.global_merge_vars = { 'VERF_LINK'  : verf_link, 'COMPANY' : 'Questr Co', 'FIRST_NAME' : first_name , }

    return email_template

def send_verification_email(user, verf_link):
    """
    Send a verification email to the user.
    """
    ##Mailchimp Template Name##
    template_name = "Welcome_Email"
    try:
        msg = __get_verification_template(template_name, user.first_name, user.email, verf_link)
        logging.warn("Assumption email Sent")
        msg.send()
    except Exception, e:
        logging.exception(str(e))