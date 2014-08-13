

import logging
from django.core.mail import EmailMessage

def _load_template(user, email_details):
    """
    Returns the template for email verification.
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
    Send a verification email to the user.
    """
    ##Mailchimp Template Name##
    # email_details = {
    #                     'subject' : subject,
    #                     'template_name' : template_name,
    #                     'global_merge_vars': {
    #                                             'quest_public_link' : quest.public_link,
    #                                             'quest_description' : quest.description,
    #                                             'user_first_name'   : user.first_name,
    #                                             'email_unsub_link'  : questr_unsubscription_link,
    #                                             'quest_title'       : quest.title,
    #                                             'quest_reward'      : quest.reward,
    #                                             'quest_browse_link' : quest_browse_link,
    #                                             'quest_support_mail': quest.support_email,
    #                                             'recipient_id'      : user.id,
    #                                             'company'           : "Questr Co"

    #                                             },
    #                 }
    try:
        msg = _load_template(user, email_details)
        msg.send()
        logging.warn("Notification sent to - %s for %s", user.email, email_details['template_name'])
    except Exception, e:
        logging.warn("Error during sending of Email to - %s for %s", user.email, email_details['template_name'])
        logging.warn("Error message is %s", str(e))


def _load_contact_template(user_email, email_details):
    """
    Returns the template for email verification.
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
    Send a verification email to the user.
    """
    ##Mailchimp Template Name##
    # email_details = {
    #                     'subject' : subject,
    #                     'template_name' : template_name,
    #                     'global_merge_vars': {
    #                                             'quest_public_link' : quest.public_link,
    #                                             'quest_description' : quest.description,
    #                                             'user_first_name'   : user.first_name,
    #                                             'email_unsub_link'  : questr_unsubscription_link,
    #                                             'quest_title'       : quest.title,
    #                                             'quest_reward'      : quest.reward,
    #                                             'quest_browse_link' : quest_browse_link,
    #                                             'quest_support_mail': quest.support_email,
    #                                             'recipient_id'      : user.id,
    #                                             'company'           : "Questr Co"

    #                                             },
    #                 }
    try:
        msg = _load_contact_template(user_email, email_details)
        logging.warn("Notification sent to - %s for %s", user_email, email_details['template_name'])
        msg.send()
    except Exception, e:
        logging.exception(str(e))