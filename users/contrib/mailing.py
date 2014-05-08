

import logging
from django.core.mail import EmailMultiAlternatives#, send_mail


def __get_verification_template(email, verf_link, attach_alternative=False):
    """
    Returns the template for email verification.
    """
    email_template = EmailMultiAlternatives(
        subject="Questr email verification",
        body="Welcome to the world of peer to peer delivery service.Please click this link {0} to confirm your verification and connect with questerians.".format(verf_link),
        from_email="Questr <questr@dev.co>",
        to=[email],
        headers={'Reply-To': "Service <support@questr.com>"}
        )
    if attach_alternative:
        email_template.attach_alternative("<p>Test test</p>", "text/html")

        # Optional Mandrill-specific extensions:
        email_template.tags = ["one tag", "two tag", "red tag", "blue tag"]
        # email_template.metadata = {'user_id': "8675309"}

    return email_template

def send_verification_email(email, verf_link):
    """
    Send a verification email to the user.
    """
    try:
        msg = __get_verification_template(email, verf_link)
        logging.warn("Assumption email Sent")
        msg.send()
    except Exception, e:
        logging.exception(str(e))
