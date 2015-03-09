'''

This is an estimator for shipping costs based on distance and type, and,

Also to show how much commission Questr is going to take from each package, current proposal:
a. Under $10: $2
b. $15.01 ~:  20%

'''

import sys
import math

# SIZE: 0 for Filing Bag, 1 for Moving Box, 2 for Extra Large
SIZE = int(sys.argv[1])
DISTANCE = float(sys.argv[2])

# Base price - box
# Distance intervals          0-5,   5.01-10, 10.01-15, 15.01-20, 20.01-25, 25.01-30, 30.01-35, 35.01-40, 40.01-45, 45+
pricing_Minutes_small    =   [6.0,   0.7,     0.7,      0.7,      0.7,      0.6,      0.6,      0.6,      0.6,      0.6]
pricing_Minutes_regular  =   [8.0,   0.8,     0.8,      0.8,      0.8,      0.7,      0.7,      0.7,      0.7,      0.7]
pricing_Minutes_large    =   [10.0,  1.0,     1.0,      1.0,      1.0,      0.8,      0.8,      0.8,      0.8,      0.8]

def shippingFee_Minutes(distance):
    charge = 0.0

    if SIZE is 0:
        if distance <= 5.0:
            charge = 6.0
        else:
            #Calculate shipping fee for the part that is divisible by 5
            for i in xrange(0, int(math.ceil(distance/5))-1):
                if i == 0:
                    charge += pricing_Minutes_small[0]
                elif i >= 9:
                    charge += pricing_Minutes_small[9]*5
                else:
                    charge += pricing_Minutes_small[i]*5

        #Calculate shipping fee for the part that is not divisible by 5, aka the tail
        if distance <= 50 and distance > 5:
            charge += pricing_Minutes_small[int(math.ceil(distance/5))-1] * float(distance%5)
        elif distance > 50:
            charge += pricing_Minutes_small[9] * float(distance%5)

        #Round the shipping fee to 2 decimal places
        charge = round(charge, 2)

    elif SIZE is 1:
        if distance <= 5.0:
            charge = 8.0
        else:
            #Calculate shipping fee for the part that is divisible by 5
            for i in xrange(0, int(math.ceil(distance/5))-1):
                if i == 0:
                    charge += pricing_Minutes_regular[0]
                elif i >= 9:
                    charge += pricing_Minutes_regular[9]*5
                else:
                    charge += pricing_Minutes_regular[i]*5

        #Calculate shipping fee for the part that is not divisible by 5, aka the tail
        if distance <= 50 and distance > 5:
            charge += pricing_Minutes_regular[int(math.ceil(distance/5))-1] * float(distance%5)
        elif distance > 50:
            charge += pricing_Minutes_regular[9] * float(distance%5)

        #Round the shipping fee to 2 decimal places
        charge = round(charge, 2)

    elif SIZE is 2:
        if distance <= 5.0:
            charge = 12.0
        else:
            #Calculate shipping fee for the part that is divisible by 5
            for i in xrange(0, int(math.ceil(distance/5))-1):
                if i == 0:
                    charge += pricing_Minutes_large[0]
                elif i >= 9:
                    charge += pricing_Minutes_large[9]*5
                else:
                    charge += pricing_Minutes_large[i]*5

        #Calculate shipping fee for the part that is not divisible by 5, aka the tail
        if distance <= 50 and distance > 5:
            charge += pricing_Minutes_large[int(math.ceil(distance/5))-1] * float(distance%5)
        elif distance > 50:
            charge += pricing_Minutes_large[9] * float(distance%5)

        #Round the shipping fee to 2 decimal places
        charge = round(charge, 2)


    return charge



#Calculate how much Questr and the courier each will be making
def income(shipping_fee):
    if shipping_fee <= 15:
        return 2;
    else:
        return round(shipping_fee*0.2, 2)

shipping_fee = shippingFee_Minutes(DISTANCE)
print("\n#### Distance: {0}km, \n#### Size: {1} (0 - Filing Bag, 1 - Moving Box, 2 - Extra Large), \n#### Shipping fee: ${2}, ".format(DISTANCE, SIZE, shipping_fee))
print("#### Questr gets ${0}, and the courier gets ${1}\n".format(income(shipping_fee), shipping_fee - income(shipping_fee)))

