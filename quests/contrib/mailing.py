

import logging
from django.core.mail import EmailMessage


def __get_quest_completion_template(template_name, user, quest, shipper_name, review_link):
    """
    Returns the template for quest completion email.
    """
    ##Email Template Init###
    email_template = EmailMessage(
        subject="Quest has been completed",
        from_email="Questr <hello@questr.co>",
        to=[user.email],
        headers={'Reply-To': "Questr <hello@questr.co>"}
        )

    ###List Email Template###
    email_template.template_name = template_name

    ###List Email Tags to be used###
    email_template.global_merge_vars = { 'REVIEW_LINK'  : review_link, 'COMPANY' : 'Questr Co', 'FIRST_NAME' : user.first_name , 
                                        'QUEST_TITLE': quest.title, 'QUEST_OFFERING': str(quest.reward), 'QUEST_SHIPPER':shipper_name}

    return email_template

def send_quest_completion_email(user, quest, shipper_name, review_link):
    """
    Send a quest completion email to the user. It also includes the review link.
    """
    ##Mailchimp Template Name##
    template_name = "Quest_Completion_Email"
    try:
        # msg = __get_quest_completion_template(template_name, user.first_name, user.email, review_link)
        msg = __get_quest_completion_template(template_name, user, quest, shipper_name, review_link)
        logging.warn("Quest Completion email Sent")
        msg.send()
    except Exception, e:
        logging.exception(str(e))