

#All Django Imports
from django.conf import settings
from django.http import Http404
from django.utils import timezone

#All local imports (libs, contribs, models)
# from quests.models import QuestPricing

#All external imports (libs, packages)
import math
import logging 

# Init Logger
logger = logging.getLogger(__name__)


class WebPricing(object):
    """
    Handles the web pricing.
    """
    def __init__(self):
        self.pricing_minutes = [10.0, 1.0,     1.0,      1.0,      0.8,      0.8,      0.8,      0.6,      0.6,      0.6]
        self.pricing_Minutes_small    =   [6.0,   0.7,     0.7,      0.7,      0.7,      0.6,      0.6,      0.6,      0.6,      0.6]
        self.pricing_Minutes_regular  =   [8.0,   0.8,     0.8,      0.8,      0.8,      0.7,      0.7,      0.7,      0.7,      0.7]
        self.pricing_Minutes_large    =   [10.0,  1.0,     1.0,      1.0,      1.0,      0.8,      0.8,      0.8,      0.8,      0.8]


    def get_price(self, distance, size='car'):
        SIZE = str(size).lower()
        """
        Returns price depending on the type of shipment and distance.
        size 0 = filing bag
        size 1 = moving box
        size 2 = extra large
        """
        charge = 0.0

        if SIZE == 'car':
            if distance <= 5.0:
                charge = 6.0
            else:
                #Calculate shipping fee for the part that is divisible by 5
                for i in xrange(0, int(math.ceil(distance/5))-1):
                    if i == 0:
                        charge += self.pricing_Minutes_small[0]
                    elif i >= 9:
                        charge += self.pricing_Minutes_small[9]*5
                    else:
                        charge += self.pricing_Minutes_small[i]*5

            #Calculate shipping fee for the part that is not divisible by 5, aka the tail
            if distance <= 50 and distance > 5:
                charge += self.pricing_Minutes_small[int(math.ceil(distance/5))-1] * float(distance%5)
            elif distance > 50:
                charge += self.pricing_Minutes_small[9] * float(distance%5)

            #Round the shipping fee to 2 decimal places
            charge = round(charge, 2)

        elif SIZE == 'van':
            if distance <= 5.0:
                charge = 8.0
            else:
                #Calculate shipping fee for the part that is divisible by 5
                for i in xrange(0, int(math.ceil(distance/5))-1):
                    if i == 0:
                        charge += self.pricing_Minutes_regular[0]
                    elif i >= 9:
                        charge += self.pricing_Minutes_regular[9]*5
                    else:
                        charge += self.pricing_Minutes_regular[i]*5

            #Calculate shipping fee for the part that is not divisible by 5, aka the tail
            if distance <= 50 and distance > 5:
                charge += self.pricing_Minutes_regular[int(math.ceil(distance/5))-1] * float(distance%5)
            elif distance > 50:
                charge += self.pricing_Minutes_regular[9] * float(distance%5)

            #Round the shipping fee to 2 decimal places
            charge = round(charge, 2)

        elif SIZE == 'minivan':
            if distance <= 5.0:
                charge = 12.0
            else:
                #Calculate shipping fee for the part that is divisible by 5
                for i in xrange(0, int(math.ceil(distance/5))-1):
                    if i == 0:
                        charge += self.pricing_Minutes_large[0]
                    elif i >= 9:
                        charge += self.pricing_Minutes_large[9]*5
                    else:
                        charge += self.pricing_Minutes_large[i]*5

            #Calculate shipping fee for the part that is not divisible by 5, aka the tail
            if distance <= 50 and distance > 5:
                charge += self.pricing_Minutes_large[int(math.ceil(distance/5))-1] * float(distance%5)
            elif distance > 50:
                charge += self.pricing_Minutes_large[9] * float(distance%5)

            #Round the shipping fee to 2 decimal places
            charge = round(charge, 2)


        return charge
