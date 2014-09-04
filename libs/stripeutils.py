

import os
import stripe
import logging

class PayStripe(object):
    """Handles the payment using Stripe"""
    def charge(self, token, amount):
        try:
            stripe.api_key=os.environ['STRIPE_TEST_SECRET_KEY']
            charge = stripe.Charge.create(
                        amount = amount,
                        currency = "cad",
                        card = token,
                        description = "Payment to Questr via form"
                        )
        except stripe.error.CardError, e:
            body = e.json_body
            error = body['error']
            responsedict = {}
            responsedict['status'] = "fail"
            responsedict['type'] = error['type']
            responsedict['message'] = error['message']
            logging.warn(responsedict)
            return responsedict
        except stripe.error.InvalidRequestError, e:
            body = e.json_body
            error = body['error']
            responsedict = {}
            responsedict['status'] = "fail"
            responsedict['type'] = error['type']
            responsedict['message'] = error['message']
            logging.warn(responsedict)
            return responsedict
        except stripe.error.StripeError, e:
            responsedict = {}
            responsedict['status'] = "fail"
            responsedict['code'] = "Generic_Error"
            responsedict['type'] = "Stripe_Error"
            responsedict['message'] = e
            logging.warn(responsedict)
            return responsedict
        except Exception, e:
            responsedict = {}
            responsedict['status'] = "fail"
            responsedict['code'] = "Other_Error"
            responsedict['type'] = "System_Error"
            responsedict['message'] = e
            logging.warn(responsedict)
            return responsedict

        responsedict = {}
        responsedict['status'] = "pass"
        return responsedict