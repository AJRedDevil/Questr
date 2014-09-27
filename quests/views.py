from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from libs import email_notifier, geomaps, pricing, stripeutils
from users.access.requires import verified


from .contrib import quest_handler
from users.contrib.user_handler import isShipper, getShippers, getQuestrDetails
from users.contrib import user_handler
from .forms import QuestCreationForm, QuestChangeForm, QuestConfirmForm, DistancePriceForm
from .models import Quests

import logging
logger = logging.getLogger(__name__)

import simplejson as json

@verified
@login_required
def listallquests(request):
    # pagetype="loggedin"
    # user = request.user
    # allquests = Quests.objects.all()
    # return render(request, 'listallquest.html', locals())
    pagetitle="home"
    return redirect("home")

@verified
@login_required
def viewquest(request, questname):
    pagetype="loggedin"
    user = request.user
    questname=questname
    try:
        questdetails = Quests.objects.get(id=questname)
        pagetitle = questdetails.title
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        isOwner = True

    pagetitle=questdetails.title
    isShipperForQuest=quest_handler.isShipperForQuest(str(user.id), questname)
    return render(request, 'viewquest.html', locals())

@verified
@login_required
def editquest(request, questname):
    pagetype="loggedin"
    user = request.user
    questname=questname
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    if questdetails.shipper:
        # This has to return a message [ The quest has already been applied for, can't be edited now ]
        # Later on any edits by any Questr should notify the shippers.
        return redirect('home')

    if request.method=="POST":
        # if questdetails.questrs.id == request.user.id:
        #     instance=get_object_or_404(Quests, id=questname)
        #     user_form = QuestChangeForm(data=request.POST, instance=instance)
        #     # logger.debug(user_form.errors)
        #     # logger.debug(user_form.is_valid())
        #     if user_form.is_valid():
        #         quest_data = user_form.save(commit=False)
        #         quest_data.save()
        #         message = "Your quest has been updated!"
        #         return redirect('viewquest', questname=questname)
        pagetype="loggedin"
        if questdetails.questrs.id == user.id:
            instance=get_object_or_404(Quests, id=questname)
            user_form = QuestChangeForm(data=request.POST, instance=instance)
            # logger.debug(user_form.errors)
            # logger.debug(user_form.is_valid())
            # logger.debug(user_form)
            if user_form.is_valid():
                title = user_form.cleaned_data['title']
                description = user_form.cleaned_data['description']
                srccity = user_form.cleaned_data['srccity']
                srcaddress = user_form.cleaned_data['srcaddress']
                srcpostalcode = user_form.cleaned_data['srcpostalcode']
                srcname = user_form.cleaned_data['srcname']
                srcphone = user_form.cleaned_data['srcphone']
                dstcity = user_form.cleaned_data['dstcity']
                dstaddress = user_form.cleaned_data['dstaddress']
                dstpostalcode = user_form.cleaned_data['dstpostalcode']
                dstname = user_form.cleaned_data['dstname']
                dstphone = user_form.cleaned_data['dstphone']
                size = user_form.cleaned_data['size']
                # For distance
                #the distance and price hsa to be set up into a temp database, also the 
                #image file needs to be on a temp folder for processign to reduce API calls
                maps = geomaps.GMaps()
                origin = srcaddress+', '+srccity+', '+srcpostalcode
                destination = dstaddress+', '+dstcity+', '+dstpostalcode
                maps.set_geo_args(dict(origin=origin, destination=destination))
                distance = maps.get_total_distance()
                map_image = maps.fetch_static_map()
                # For price
                price = pricing.WebPricing()
                reward = price.get_price(distance, shipment_mode=size)
                pagetitle = "Confirm your Quest"
                return render(request, 'confirmquestedit.html', locals())  
            if user_form.errors:
                logger.debug("Form has errors, %s ", user_form.errors)

        pagetitle="Edit - " + questdetails.title
        return render(request, 'editquest.html', locals())  

    # Check if the owner and the user are the same
    if questdetails.questrs.id == user.id:
        pagetitle="Edit - " + questdetails.title
        return render(request, 'editquest.html', locals())

    raise Http404
    return render(request,'404.html')

@verified
@login_required
def confirmeditquest(request, questname):
    pagetype="loggedin"
    user = request.user
    questname=questname
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    if request.method=="POST":
        # if questdetails.questrs.id == request.user.id:
        #     instance=get_object_or_404(Quests, id=questname)
        #     user_form = QuestChangeForm(data=request.POST, instance=instance)
        #     # logger.debug(user_form.errors)
        #     # logger.debug(user_form.is_valid())
        #     if user_form.is_valid():
        #         quest_data = user_form.save(commit=False)
        #         quest_data.save()
        #         message = "Your quest has been updated!"
        #         return redirect('viewquest', questname=questname)
        from users.contrib.user_handler import getShipper
        pagetype="loggedin"
        if questdetails.questrs.id == user.id:
            instance=get_object_or_404(Quests, id=questname)
            user_form = QuestConfirmForm(data=request.POST, instance=instance)
            if user_form.is_valid():
                pickupdict = {}
                dropoffdict = {}
                size = user_form.cleaned_data['size']
                srccity = user_form.cleaned_data['srccity']
                srcaddress = user_form.cleaned_data['srcaddress']
                quest_data = user_form.save(commit=False)
                srcpostalcode = user_form.cleaned_data['srcpostalcode']
                srcname = user_form.cleaned_data['srcname']
                srcphone = user_form.cleaned_data['srcphone']
                dstcity = user_form.cleaned_data['dstcity']
                dstaddress = user_form.cleaned_data['dstaddress']
                dstpostalcode = user_form.cleaned_data['dstpostalcode']
                dstname = user_form.cleaned_data['dstname']
                dstphone = user_form.cleaned_data['dstphone']
                ## categorizing source and destination info
                pickupdict['city'] = srccity
                pickupdict['address'] = srcaddress
                pickupdict['postalcode'] = srcpostalcode
                pickupdict['name'] = srcname
                pickupdict['phone'] = srcphone
                dropoffdict['city'] = dstcity
                dropoffdict['address'] = dstaddress
                dropoffdict['postalcode'] = dstpostalcode
                dropoffdict['name'] = dstname
                dropoffdict['phone'] = dstphone
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
                reward = price.get_price(distance, shipment_mode=size)
                quest_data = user_form.save(commit=False)
                ##Submit dict to the field
                ##Submit dict to the field
                # logger.debug("Pickup dict %s", pickupdict)
                # logger.debug("Dropoff dict %s", dropoffdict)
                quest_data = user_form.save(commit=False)
                quest_data.pickup = json.dumps(pickupdict)
                quest_data.dropoff = json.dumps(dropoffdict)
                quest_data.map_image = map_image
                quest_data.reward=reward
                quest_data.item_images = user_form.cleaned_data['item_images']
                quest_data.map_image = map_image
                quest_data.save()
                pagetitle = "Confirm your Quest"
                return redirect(viewquest, questname=questdetails.id)
            if user_form.errors:
                logger.debug("Form has errors, %s ", user_form.errors)
        pagetitle="Edit - " + questdetails.title
        return redirect('editquest',questname=questdetails.id)

    # Check if the owner and the user are the same
    if questdetails.questrs.id == user.id:
        pagetitle="Edit - " + questdetails.title
        return redirect('editquest',questname=questdetails.id)

    raise Http404
    return render(request,'404.html')

@verified
@login_required
def newquest(request):
    """creates new quest and sends notification to shippers"""
    from users.contrib.user_handler import getShipper
    pagetype="loggedin"
    user = request.user

    if request.method=="POST":
        now = timezone.now()
        user_form = QuestCreationForm(request.POST)
        # logger.debug(user_form.errors)
        # logger.debug(user_form.is_valid())
        # logger.debug(user_form)
        if user_form.is_valid():
            # logger.debug(user_form.fields)
            title = user_form.cleaned_data['title']
            size = user_form.cleaned_data['size']
            description = user_form.cleaned_data['description']
            srccity = user_form.cleaned_data['srccity']
            srcaddress = user_form.cleaned_data['srcaddress']
            srcpostalcode = user_form.cleaned_data['srcpostalcode']
            srcname = user_form.cleaned_data['srcname']
            srcphone = user_form.cleaned_data['srcphone']
            dstcity = user_form.cleaned_data['dstcity']
            dstaddress = user_form.cleaned_data['dstaddress']
            dstpostalcode = user_form.cleaned_data['dstpostalcode']
            dstname = user_form.cleaned_data['dstname']
            dstphone = user_form.cleaned_data['dstphone']
            # For distance
            #the distance and price hsa to be set up into a temp database, also the 
            #image file needs to be on a temp folder for processign to reduce API calls
            maps = geomaps.GMaps()
            origin = srcaddress+', '+srccity+', '+srcpostalcode
            destination = dstaddress+', '+dstcity+', '+dstpostalcode
            maps.set_geo_args(dict(origin=origin, destination=destination))
            distance = maps.get_total_distance()
            map_image = maps.fetch_static_map()
            logger.debug(map_image)
            # For price
            price = pricing.WebPricing()
            reward = price.get_price(distance, shipment_mode=size)
            pagetitle = "Confirm your Quest"
            return render(request, 'confirmquest.html', locals())  
        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)

    pagetitle = "Create your Quest"
    return render(request, 'newquest.html', locals())  

@verified
@login_required
def confirmquest(request):
    """creates new quest and sends notification to shippers"""
    from users.contrib.user_handler import getShipper
    pagetype="loggedin"
    user = request.user

    if request.method=="POST":
        now = timezone.now()
        user_form = QuestConfirmForm(request.POST, request.FILES)
        if user_form.is_valid():
            pickupdict = {}
            dropoffdict = {}
            size = user_form.cleaned_data['size']
            srccity = user_form.cleaned_data['srccity']
            srcaddress = user_form.cleaned_data['srcaddress']
            srcpostalcode = user_form.cleaned_data['srcpostalcode']
            srcname = user_form.cleaned_data['srcname']
            srcphone = user_form.cleaned_data['srcphone']
            dstcity = user_form.cleaned_data['dstcity']
            dstaddress = user_form.cleaned_data['dstaddress']
            dstpostalcode = user_form.cleaned_data['dstpostalcode']
            dstname = user_form.cleaned_data['dstname']
            dstphone = user_form.cleaned_data['dstphone']
            ## categorizing source and destination info
            pickupdict['city'] = srccity
            pickupdict['address'] = srcaddress
            pickupdict['postalcode'] = srcpostalcode
            pickupdict['name'] = srcname
            pickupdict['phone'] = srcphone
            dropoffdict['city'] = dstcity
            dropoffdict['address'] = dstaddress
            dropoffdict['postalcode'] = dstpostalcode
            dropoffdict['name'] = dstname
            dropoffdict['phone'] = dstphone
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
            reward = price.get_price(distance, shipment_mode=size)
            quest_data = user_form.save(commit=False)
            ##Submit dict to the field
            quest_data.pickup = json.dumps(pickupdict)
            quest_data.dropoff = json.dumps(dropoffdict)
            quest_data.questrs_id=request.user.id
            quest_data.creation_date=now
            quest_data.reward=reward
            quest_data.item_images = user_form.cleaned_data['item_images']
            quest_data.map_image = map_image
            quest_data.save()
            # return redirect('pay',questname=quest_data)
            try:
                # shippers = getShippers()
                # for shipper in shippers: # send notifcations to all the shippers
                #     email_details = quest_handler.prepNewQuestNotification(shipper, quest_data)
                #     email_notifier.send_email_notification(shipper, email_details)
                couriermanager = user_handler.CourierManager()
                couriermanager.informShippers(quest_data)
            except Exception, e:
                ##Inform admin of an error
                logger.debug(e)
                pass
            quest_handler.update_resized_image(quest_data.id)
            message="Your quest has been created!"
            logger.debug(message)
            return redirect('home')

        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)

    pagetitle = "Create a Quest"
    message="There were some errors creating your quest, please try again !"
    return redirect('home')

@verified
@login_required
def applyForQuest(request, questname):
    """Takes in applications for a quest"""
    pagetype="loggedin"
    shipper = request.user # the guy logged in is the shipper
    questname = questname
    try:
        questdetails = Quests.objects.get(id=questname, isaccepted=False)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        return redirect('home')

    # get questr information
    questr = getQuestrDetails(questdetails.questrs_id)
    # add a shipper to the quest
    quest_handler.addShipper(str(shipper.id), questname)
    email_details = quest_handler.prepQuestAppliedNotification(shipper, questr, questdetails)
    email_notifier.send_email_notification(questr, email_details)

    message="Your application has been sent to the quest owner"
    logger.debug(message)
    return redirect('viewquest', questname=questname)

@verified
@login_required
def withdrawFromQuest(request, questname):
    """Takes in applications for a quest"""
    pagetype="loggedin"
    shipper = request.user # the guy logged in is the shipper
    questname = questname
    try:
        questdetails = Quests.objects.get(id=questname, isaccepted=False)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        return redirect('home')
    # remove the shipper from the quest
    quest_handler.delShipper(str(shipper.id), questname)
    message="You have retracted yourself from the quest"
    logger.debug(message)
    return redirect('viewquest', questname=questname)

@verified
@login_required
def deletequest(request, questname):
    """Deletes the quest
    """
    pagetitle="home"
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    if questdetails.questrs.id == request.user.id:
        message=""
        if questdetails.isaccepted:
            message="Your quest has been accepted."
        elif questdetails.shipper:
            message="Shipper have applied to your quest."
        if not message:
            try:
                Quests.objects.filter(id=questname).update(ishidden=True)
            except Quests.DoesNotExist:
                raise Http404
                return render(request,'404.html')
            message = "Your quest has been deleted!"
            return redirect('home')
        else:
            return redirect('viewquest', questname=questname)
    return redirect("home")

@verified
@login_required
def completequest(request, questname):
    """Verify delivery code and set the quest as completed
    Send the notification to the offerer and also the review link
    """
    #if already completed ignore
    pagetype="loggedin"
    if request.method == "POST":
        shipper = request.user
        questname = questname
        if quest_handler.isShipperForQuest(str(shipper.id), questname):
            try:
                questdetails = Quests.objects.get(id=questname, isaccepted=True)
            except Quests.DoesNotExist:
                logger.debug("Quest not found")
                raise Http404
                return render(request,'404.html')
            # Check if the owner and the user are the same
            if questdetails.questrs.id == request.user.id:
                return redirect('home')

            if questdetails.status != 'Accepted':
                return redirect('home')
            
            delivery_code = request.POST['delivery_code']
            # verify delivery code
            if delivery_code:
                if questdetails.delivery_code != delivery_code:
                    message = "Provided delivery code. Please enter the correct delivery code." 
                    logger.debug("Provided delivery code \'%s\' doesn't match the one in the quest number %s", delivery_code, questdetails.id)
                    logger.debug("returned to viewquest page of %s", questname)
                    return redirect('viewquest', questname=questname) # return with message
                else:
                    questr = getQuestrDetails(questdetails.questrs_id)
                    Quests.objects.filter(id=questname).update(status='Completed')
                    Quests.objects.filter(id=questname).update(is_complete='t')

                    ## Update the delivered date
                    now = timezone.now()
                    Quests.objects.filter(id=questname).update(delivery_date=now)

                    ## Reload questdetails to get in the delivery date from quest
                    try:
                        questdetails = Quests.objects.get(id=questname, isaccepted=True)
                    except Quests.DoesNotExist:
                        logger.debug("Quest not found")
                        raise Http404
                        return render(request,'404.html')
                    
                    ## Send notification to shipper
                    questr_review_link = quest_handler.get_review_link(questname, questr.id)
                    email_details = quest_handler.prepQuestCompleteNotification(shipper, questr, questdetails, questr_review_link)
                    email_notifier.send_email_notification(shipper, email_details)
                    logger.debug("Quest completion email has been sent to %s", shipper.email)
                    ## Send notification to questr
                    shipper_review_link = quest_handler.get_review_link(questname, shipper.id)
                    email_details = quest_handler.prepQuestCompleteNotification(questr, questr, questdetails, shipper_review_link)
                    email_notifier.send_email_notification(questr, email_details)
                    logger.debug("Quest completion email has been sent to %s", questr.email)
                    message="Quest completion mail has been sent to the Offerer."
                    return redirect('viewquest', questname=questname) # display message

            return redirect('viewquest', questname=questname)
        else:
            message = "Imposter detected" # Correct message required
            logger.debug(message)
            return redirect('viewquest', questname=questname)
    return redirect('viewquest', questname=questname)

# @verified
# @login_required
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
            # For distance
            #the distance and price hsa to be set up into a temp database, also the 
            #image file needs to be on a temp folder for processign to reduce API calls
            maps = geomaps.GMaps()
            origin = srcaddress+', '+srccity+', '+srcpostalcode
            destination = dstaddress+', '+dstcity+', '+dstpostalcode
            maps.set_geo_args(dict(origin=origin, destination=destination))
            distance = maps.get_total_distance()
            # For price
            price = pricing.WebPricing()
            reward = price.get_price(distance, shipment_mode=size)
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
