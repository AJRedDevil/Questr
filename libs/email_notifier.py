

import logging
logger = logging.getLogger(__name__)

from django.core.mail import EmailMessage


def _load_template(user, email_details):
    """
    Loads the email contents and returns the template for email
    """
    ##Email Template Init###
    email_template = EmailMessage(
        subject=email_details['subject'],
        from_email="Questr <hello@questr.co>",
        to=[user.email],
        headers={'Reply-To': "Questr <hello@questr.co>"}
    )

    ###List Email Template###
    email_template.template_name = email_details['template_name']

    ###List Email Tags to be used###
    email_template.global_merge_vars = email_details['global_merge_vars']

    return email_template


def send_email_notification(user, email_details):
    """
    Send a notification email to the user.
    """
    try:
        msg = _load_template(user, email_details)
        msg.send()
        logger.debug("Notification sent to - %s for %s", user.email, email_details['template_name'])
    except Exception, e:
        logger.warn("Error during sending of Email to - %s for %s", user.email, email_details['template_name'])
        logger.warn("Error message is %s", str(e))


def _load_contact_template(user_email, email_details):
    """
    Loads the email contents and returns the template for contact us
    """
    ##Email Template Init###
    email_template = EmailMessage(
        subject=email_details['subject'],
        from_email="Questr <hello@questr.co>",
        to=["Questr <hello@questr.co>"],
        headers={'Reply-To': "Questr <hello@questr.co>"}
    )

    ###List Email Template###
    email_template.template_name = email_details['template_name']

    ###List Email Tags to be used###
    email_template.global_merge_vars = email_details['global_merge_vars']

    return email_template


def send_contactus_notification(user_email, email_details):
    """
    Send a contact us notification
    """
    try:
        msg = _load_contact_template(user_email, email_details)
        logger.warn("Notification sent to - %s for %s", user_email, email_details['template_name'])
        msg.send()
    except Exception, e:
        logger.warn("Error during sending of Email to - %s for %s", user_email, email_details['template_name'])
        logger.warn("Error message is %s", str(e))


def _load_signup_invitation_template(user_email, email_details):
    """
    Loads the email contents and returns the template for contact us
    """
    ##Email Template Init###
    email_template = EmailMessage(
        subject=email_details['subject'],
        from_email="Questr <hello@questr.co>",
        to=[user_email],
        headers={'Reply-To': "Questr <hello@questr.co>"}
    )

    ###List Email Template###
    email_template.template_name = email_details['template_name']

    ###List Email Tags to be used###
    email_template.global_merge_vars = email_details['global_merge_vars']

    return email_template


def send_signup_invitation(user_email, email_details):
    """
    Send a contact us notification
    """
    try:
        msg = _load_signup_invitation_template(user_email, email_details)
        logger.debug("Notification sent to - %s for %s", user_email, email_details['template_name'])
        msg.send()
    except Exception, e:
        logger.warn("Error during sending of Email to - %s for %s", user_email, email_details['template_name'])
        logger.warn("Error message is %s", str(e))
