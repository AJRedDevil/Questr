

#All Django Imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

#All local imports (libs, contribs, models)
from .contrib import quest_handler
from .forms import QuestCreationForm, QuestConfirmForm, DistancePriceForm, TrackingNumberSearchForm
from .models import Quests, QuestTransactional
from libs import geomaps, pricing, stripeutils
from users.access.requires import verified, is_quest_alive
from users.contrib import user_handler
from users.models import QuestrUserProfile
from quests.tasks import init_courier_selection, checkstatus, send_complete_quest_link

#All external imports (libs, packages)
import logging
from datetime import timedelta
import simplejson as json
import os
import pytz

# Init Logger
logger = logging.getLogger(__name__)

@verified
@login_required
def viewquest(request, questname):
    """
    View details of a Quest
    """
    user = request.user
    questdetails = quest_handler.getQuestDetails(questname)
    pagetitle = questdetails.title
    if 'alert_message' in request.session:
        alert_message = request.session.get('alert_message')
        del request.session['alert_message']
    # Only allow a superuser, a shipper assigned for the quest,
    # or the user who created the shipment view the shipment
    if (questdetails.shipper == str(user.id) or
            user.is_superuser is True or questdetails.questrs_id == user.id):
    # Check if the owner and the user are the same
        if questdetails.questrs.id == request.user.id:
            isOwner = True
        pagetitle = questdetails.title
        return render(request, 'viewquest.html', locals())
    else:
        return redirect('home')


@verified
@login_required
def newquest(request):
    """creates new quest and sends notification to shippers"""
    user = request.user
    if user.is_shipper:
        return redirect('home')

    if request.method == "POST":
        # logging.warn(request.POST)
        user_form = QuestCreationForm(request.POST)
        if user_form.is_valid():
            title = user_form.cleaned_data['title']
            size = user_form.cleaned_data['size']
            description = user_form.cleaned_data['description']
            srccity = user_form.cleaned_data['srccity']
            srcaddress = user_form.cleaned_data['srcaddress']
            srcaddress_2 = user_form.cleaned_data['srcaddress_2']
            srcpostalcode = user_form.cleaned_data['srcpostalcode']
            srcname = user_form.cleaned_data['srcname']
            srcphone = user_form.cleaned_data['srcphone']
            dstcity = user_form.cleaned_data['dstcity']
            dstaddress = user_form.cleaned_data['dstaddress']
            dstaddress_2 = user_form.cleaned_data['dstaddress_2']
            dstpostalcode = user_form.cleaned_data['dstpostalcode']
            dstname = user_form.cleaned_data['dstname']
            dstphone = user_form.cleaned_data['dstphone']
            # For distance
            maps = geomaps.GMaps()
            origin = srcaddress+', '+srccity+', '+srcpostalcode
            destination = dstaddress+', '+dstcity+', '+dstpostalcode
            maps.set_geo_args(dict(origin=origin, destination=destination))
            distance = maps.get_total_distance()
            logger.warn(distance)
            map_image = maps.fetch_static_map()
            logger.warn(map_image)
            if distance is None or map_image is None:
                request.session['alert_message'] = dict(type="Danger",message="An error occured while creating your shipment, please try again in a while!")
                message = "Error occured while creating quest"
                warnlog = dict(message=message)
                logger.warn(warnlog)
                return redirect('home')
            # For price
            price = pricing.WebPricing()
            reward = price.get_price(distance, size=size)
            stripereward = reward*100
            pagetitle = "Confirm your Quest"
            return render(request, 'confirmquest.html', locals())  
        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)
            return render(request, 'newquest.html', locals())
           
    user_form = QuestCreationForm()
    pagetitle = "Create your Quest"
    return render(request, 'newquest.html', locals())  

@verified
@login_required
def confirmquest(request):
    """creates new quest and sends notification to shippers"""
    user = request.user
    if user.is_shipper:
        return redirect('home')

    if request.method=="POST":
        user_form = QuestConfirmForm(request.POST, request.FILES)
        if user_form.is_valid():
            pickupdict = {}
            dropoffdict = {}
            size = user_form.cleaned_data['size']
            srccity = user_form.cleaned_data['srccity']
            srcaddress = user_form.cleaned_data['srcaddress']
            srcaddress_2 = user_form.cleaned_data['srcaddress_2']
            srcpostalcode = user_form.cleaned_data['srcpostalcode']
            srcname = user_form.cleaned_data['srcname']
            srcphone = user_form.cleaned_data['srcphone']
            dstcity = user_form.cleaned_data['dstcity']
            dstaddress = user_form.cleaned_data['dstaddress']
            dstaddress_2 = user_form.cleaned_data['dstaddress_2']
            dstpostalcode = user_form.cleaned_data['dstpostalcode']
            dstname = user_form.cleaned_data['dstname']
            dstphone = user_form.cleaned_data['dstphone']
            ## categorizing source and destination info
            pickupdict['city'] = srccity
            pickupdict['address'] = srcaddress
            pickupdict['address_2'] = srcaddress_2
            pickupdict['postalcode'] = srcpostalcode
            pickupdict['name'] = srcname
            pickupdict['phone'] = srcphone
            dropoffdict['city'] = dstcity
            dropoffdict['address'] = dstaddress
            dropoffdict['address_2'] = dstaddress_2
            dropoffdict['postalcode'] = dstpostalcode
            dropoffdict['name'] = dstname
            dropoffdict['phone'] = dstphone
            # Pickup Time
            # pickup_time = user_form.cleaned_data['pickup_time'].lower()
            # Recalculate distance and price to prevent any arbitrary false attempt.
            # For distance
            maps = geomaps.GMaps()
            origin = srcaddress+', '+srccity+', '+srcpostalcode
            destination = dstaddress+', '+dstcity+', '+dstpostalcode
            maps.set_geo_args(dict(origin=origin, destination=destination))
            distance = maps.get_total_distance()
            map_image = maps.fetch_static_map()
            # For price
            price = pricing.WebPricing()
            reward = price.get_price(distance, size=size)
            quest_data = user_form.save(commit=False)
            ##Submit dict to the field
            quest_data.pickup = json.dumps(pickupdict)
            quest_data.dropoff = json.dumps(dropoffdict)
            quest_data.questrs_id=request.user.id
            quest_data.reward=reward
            quest_data.item_images = user_form.cleaned_data['item_images']
            quest_data.map_image = map_image
            # pickup_time = user_form.cleaned_data['pickup_time']
            # if pickup_time == 'now':
            #     pickup_time = quest_handler.get_pickup_time()
            # elif pickup_time == 'not_now':
            #     pickup_when = user_form.cleaned_data['pickup_when']
            #     time = user_form.cleaned_data['not_now_pickup_time']
            #     pickup_time = quest_handler.get_pickup_time(pickup_time, pickup_when, time)
            #     if (pickup_time - timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))).total_seconds() < 0:
            #         request.session['alert_message'] = dict(type="warning",message="Pickup time cannot be before current time!")
            #         return redirect('home')
            #     # If the p
            #     if (pickup_time - timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))).total_seconds() < 3600:
            #         pickup_time = quest_handler.get_pickup_time()
            # else:
            #     pickup_time = quest_handler.get_pickup_time()
            # quest_data.pickup_time = pickup_time
            try:
                chargeme = stripeutils.PayStripe()
                result = chargeme.charge(request.POST['stripeToken'],int(reward*100))
                if result['status'] == "pass":
                    quest_data.save()
                    # quest_handler.update_resized_image(quest_data.id)
                    eventmanager = quest_handler.QuestEventManager()
                    extrainfo = dict(detail="quest created")
                    eventmanager.setevent(quest_data, 1, extrainfo)
                    message="Quest {0} has been created by user {1}".format(quest_data.id, user)
                    request.session['alert_message'] = dict(type="Success",message="Your quest has been created!")
                    logger.warn(message)
                    init_courier_selection.apply_async((quest_data.id,), eta=quest_handler.get_pickup_time())
                    return redirect('home')
                else:
                    request.session['alert_message'] = dict(type="Danger",message="An error occured while creating your shipment, please try again in a while!")
                    message="Error occured while creating quest"
                    warnlog = dict(message=message, exception=e)
                    logger.warn(warnlog)
                    return redirect('home')
            except Exception, e:
                ##Inform admin of an error
                request.session['alert_message'] = dict(type="Danger",message="An error occured while creating your shipment, please try again in a while!")
                message="Error occured while creating quest"
                warnlog = dict(message=message, exception=e)
                logger.warn(warnlog)
                return redirect('home')

        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)

    pagetitle = "Confirm your quest details"
    return redirect('home')

##ONLY FOR TWILIO
@verified
@login_required
def completequest(request, questname, deliverycode):
    """
    Verify delivery code and set the quest as completed
    Send the notification to the offerer and also the review link
    """
    #if already completed ignore
    shipper = request.user
    questname = questname
    if quest_handler.isShipperForQuest(shipper, questname):
        questdetails = quest_handler.getQuestDetails(questname)
        if questdetails.isaccepted:
            # Check if the owner and the user are the same
            if questdetails.questrs.id == request.user.id:
                logger.warn("Attempted complete on {0} by the owner {1} himself!".format(questdetails.id, request.user))
                return redirect('home')

            if questdetails.status != 'Accepted':
                logger.warn("Attempted complete on an unaccepted quest {0} by {1}!".format(questdetails.id, request.user))
                return redirect('home')
            delivery_code = deliverycode
            # verify delivery code
            if delivery_code:
                if questdetails.delivery_code != delivery_code:
                    logger.warn("Provided delivery code \'%s\' doesn't match the one in the quest number %s", delivery_code, questdetails.id)
                    request.session['alert_message'] = dict(type="Danger",message="Provided delivery code is not correct!")
                    return redirect('viewquest', questname=questname) # return with message
                else:
                    Quests.objects.filter(id=questname).update(status='Completed')
                    Quests.objects.filter(id=questname).update(is_complete=True)
                    ## Update the delivered date
                    now = timezone.now()
                    Quests.objects.filter(id=questname).update(delivery_date=now)
                    ## Reload questdetails to get in the delivery date from quest
                    questdetails = quest_handler.getQuestDetails(questname)
                    logger.debug("Quest {0} has been successfully completed by {1}".format(questdetails.id, request.user))
                    eventmanager = quest_handler.QuestEventManager()
                    extrainfo = dict(detail="quest complete")
                    eventmanager.setevent(questdetails, 8, extrainfo)
                    from libs.twilio_handler import twclient
                    tw = twclient()
                    alert_message=os.environ['SMS_QUESTCOMPLETION_MSG'].format(questdetails.dropoff['address'], questdetails.dropoff['city'], questdetails.dropoff['postalcode'])
                    logger.warn(alert_message)
                    tw.sendmessage(questdetails.questrs.phone, alert_message)
                    request.session['alert_message'] = dict(type="Success",message="The Questr has been notified!")
                    return redirect('viewquest', questname=questname) # display message
        return redirect('viewquest', questname=questname)
    else:
        logger.warn("Attempted complete on an unauthorized quest {0} by {1}!".format(questdetails.id, request.user))
        return redirect('viewquest', questname=questname)


def getDistanceAndPrice(request):
    if request.method == "POST":
        user_form = DistancePriceForm(request.POST)
        if user_form.is_valid():
            srccity = user_form.cleaned_data['srccity']
            srcaddress = user_form.cleaned_data['srcaddress']
            srcpostalcode = user_form.cleaned_data['srcpostalcode']
            dstcity = user_form.cleaned_data['dstcity']
            dstaddress = user_form.cleaned_data['dstaddress']
            dstpostalcode = user_form.cleaned_data['dstpostalcode']
            size = user_form.cleaned_data['size']
            maps = geomaps.GMaps()
            origin = srcaddress+', '+srccity+', '+srcpostalcode
            destination = dstaddress+', '+dstcity+', '+dstpostalcode
            maps.set_geo_args(dict(origin=origin, destination=destination))
            distance = maps.get_total_distance()
            # For price
            price = pricing.WebPricing()
            reward = price.get_price(distance, size=size)
            resultdict = {}
            resultdict['distance'] = distance
            resultdict['price'] = reward
            return HttpResponse(json.dumps(resultdict),content_type="application/json")
        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)
            resultdict['status'] = 500
            resultdict['message'] = "Internal Server Error"
            return HttpResponse(json.dumps(resultdict),content_type="application/json")

# @verified
# @login_required
# def setnewpayment(request, questname):
#     quest_data = quest_handler.getQuestDetails(questname)
#     price = quest_data.reward
#     if request.method == "POST":
#         chargeme = stripeutils.PayStripe()
#         result = chargeme.charge(request.POST['stripeToken'],int(price*100))
#         if result['status'] == "pass":
#             return redirect('home')
#         else:
#             return redirect('pay', questname=quest_data)
    
#     return render(request, 'newpayment.html', locals())

@is_quest_alive
@login_required
def accept_quest(request, quest_code):
    """
    Verifies email of the user and redirect to the home page
    """
    user = request.user
    logger.debug(quest_code)
    if quest_code:
        try:
            transcational = QuestTransactional.objects.get(quest_code__regex=r'^%s' % quest_code)
            opptransaction = QuestTransactional.objects.get(quest_id=transcational.quest_id, \
                shipper_id=transcational.shipper_id, transaction_type=0, status=False)
            logger.debug("quest transactional")
            logger.debug(transcational)
            if transcational:
                logger.debug("transactional status")
                logger.debug(transcational.status)
                if not transcational.status:
                    try:
                        quest = Quests.objects.get(id=int(transcational.quest_id))
                        questr = user_handler.getQuestrDetails(quest.questrs_id)
                        courier = QuestrUserProfile.objects.get(id=int(transcational.shipper_id))
                        logger.debug("%s is the requesting user, where %s is the courier for %s quest" % (request.user, courier, quest))
                        if quest and courier and request.user == courier:
                            # Set status to true so it won't be used again
                            transcational.status = True
                            # Set rejection status to true so it won't be used again
                            opptransaction.status = True
                            # Set Courier status to available so he can accept multiple quests if he wants to.
                            courier.is_available = True # change this to False if you want to keep a courier as occupied
                            # Set quest's courier to respective courier
                            quest.shipper = courier.id
                            # Set quest as accepted
                            quest.isaccepted = True
                            quest.status = "Accepted"
                            ##Save all the details
                            transcational.save()
                            courier.save()
                            opptransaction.save()
                            quest.save()
                            from libs.twilio_handler import twclient
                            tw = twclient()
                            alert_message = tw.load_acceptquest_notif(quest)
                            logger.warn(alert_message)
                            tw.sendmessage(courier.phone, alert_message)
                            tw.sendmessage(questr.phone, os.environ['SMS_COURIERACCEPTANCE_MSG'])
                            # After 30 minutes send the guy a message asking if the quest is complete
                            send_complete_quest_link.apply_async((courier.id, quest.id), countdown=1800)
                            couriermanager = user_handler.CourierManager()
                            couriermanager.informCourierAfterAcceptance(courier, quest)
                            couriermanager.informQuestrAfterAcceptance(courier, questr, quest)
                            eventmanager = quest_handler.QuestEventManager()
                            extrainfo = dict(designated_courier=courier.id, detail="quest accepted by courier")
                            eventmanager.setevent(quest, 4, extrainfo)
                            request.session['alert_message'] = dict(type="success",message="Congratulations! You have accepted the quest!")
                            # Setting status of all considered couriers to True
                            considered_couriers = json.loads(quest.considered_couriers.strip(','))
                            for courier in considered_couriers:
                                courier = user_handler.getQuestrDetails(courier)
                                courier.is_available = True
                                courier.save()
                            return render(request, 'questaccepted.html',locals())
                            # return redirect('home')
                    except QuestrUserProfile.DoesNotExist:
                        logger.debug('User does not exist')
                        return redirect('home')
                else:
                    request.session['alert_message'] = dict(type="warning",message="The link has expired, perhaps you were too late to respond.")
                    return render(request, 'questtimeout.html',locals())
        except QuestTransactional.DoesNotExist:
            return redirect('home')
    return redirect('home')

@is_quest_alive
@login_required
def reject_quest(request, quest_code):
    """
        Verifies email of the user and redirect to the home page
    """
    user = request.user
    logger.debug(quest_code)
    if quest_code:
        try:
            transcational = QuestTransactional.objects.get(quest_code__regex=r'^%s' % quest_code)
            opptransaction = QuestTransactional.objects.get(quest_id=transcational.quest_id, \
                shipper_id=transcational.shipper_id, transaction_type=1, status=False)
            logger.debug("quest transactional")
            logger.debug(transcational)
            if transcational:
                logger.debug("transctional status")
                logger.debug(transcational.status)
                if not transcational.status:
                    try:
                        quest = Quests.objects.get(id=int(transcational.quest_id))
                        courier = QuestrUserProfile.objects.get(id=int(transcational.shipper_id))
                        logger.debug("%s is the requesting user, where %s is the courier for %s quest" % (request.user, courier, quest))
                        if quest and courier and request.user == courier:
                            # Set status to true so it won't be used again
                            transcational.status = True
                            # Set rejection status to true so it won't be used again
                            opptransaction.status = True
                            # Set courier status to true so he can be used for other quests    
                            # We will have to figure out another way to do this, perhaps a this courier rejected these quest type of flags
                            courier.is_available = False # This should be False, only put false for today
                            from users.tasks import activate_shipper
                            # Any courier who rejects a quest will be put on hold for 5 minutes
                            activate_shipper.apply_async((courier.id,), countdown=int(settings.REJECTED_COURIER_HOLD_TIMER))
                            # Remove this courier from the current quest's list of available shippers
                            available_couriers = quest.available_couriers
                            # logging.warn(available_couriers)
                            from libs.twilio_handler import twclient
                            tw = twclient()
                            tw.sendmessage(courier.phone, os.environ['SMS_REJECTQUEST_MSG'])
                            available_couriers.pop(str(courier.id), None)
                            quest.available_couriers = available_couriers
                            # Save all the details
                            quest.save()
                            transcational.save()
                            courier.save()
                            opptransaction.save()
                            couriermanager = user_handler.CourierManager()
                            # Re-run the shipper selection algorithm
                            quest = Quests.objects.get(id=int(transcational.quest_id))
                            couriermanager.informShippers(quest)
                            eventmanager = quest_handler.QuestEventManager()
                            extrainfo = dict(selected_courier=courier.id, detail="quest rejected by courier")
                            eventmanager.setevent(quest, 5, extrainfo)
                            return render(request, 'questrejected.html',locals())
                    except QuestrUserProfile.DoesNotExist:
                        logger.debug('User does not exist')
                        return redirect('home')
                else:
                    # request.session['alert_message'] = dict(type="warning",message="Please use the latest verification email sent, or click below to send a new email.")
                    return render(request, 'questrejected.html',locals())
        except QuestTransactional.DoesNotExist:
            return redirect('home')
    return redirect('home')

def tracking_number_search(request):
    """Searches for the tracking number"""
    if request.user.is_authenticated():
        user = request.user
        pagetype="loggedin"

    if 'tracking_number' in request.GET:
            tracking_number = request.GET['tracking_number']
            questdetails = quest_handler.getQuestDetailsByTrackingNumber(tracking_number)
            pagetitle = "Tracking your shipment"
            return render(request, 'trackingdisplay.html', locals())
    else:
        user_form = TrackingNumberSearchForm()
        pagetitle = "Enter your tracking number"
        return render(request, 'trackingsearchform.html', locals())

@verified
@login_required
def viewallquests(request):
    """Shows all the active quests so far"""
    pagetype="loggedin"
    user = request.user
    userdetails = user_handler.getQuestrDetails(user.id)
    pagetitle = "Active Quests"
    if userdetails.is_shipper:
        return redirect('home')
    else:
        quests = Quests.objects.filter(ishidden=False, isaccepted=False, questrs_id=userdetails.id, ).order_by('-creation_date')
    return render(request, 'allquestsviews.html', locals())


@verified
@login_required
def viewallactivequests(request):
    """Shows all the active quests so far"""
    pagetype="loggedin"
    user = request.user
    userdetails = user_handler.getQuestrDetails(user.id)
    pagetitle = "Active Quests"
    if userdetails.is_shipper:
        quests = Quests.objects.filter(ishidden=False, isaccepted=True, shipper=userdetails.id, is_complete=False).order_by('-creation_date')
    else:
        quests = Quests.objects.filter(ishidden=False, isaccepted=True, is_complete=False, questrs_id=userdetails.id).order_by('-creation_date')
    return render(request, 'allquestsviews.html', locals())


@verified
@login_required
def viewallpastquests(request):
    """Shows all the active quests so far"""
    pagetype = "loggedin"
    user = request.user
    userdetails = user_handler.getQuestrDetails(user.id)
    pagetitle = "Active Quests"
    if userdetails.is_shipper:
        quests = Quests.objects.filter(ishidden=False, is_complete=True, isaccepted=True, shipper=userdetails.id).order_by('-creation_date')
    else:
        quests = Quests.objects.filter(ishidden=False, is_complete=True, questrs_id=userdetails.id).order_by('-creation_date')
    return render(request, 'allquestsviews.html', locals())
