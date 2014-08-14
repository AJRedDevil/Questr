from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.decorators import login_required

from libs import email_notifier, geomaps, pricing

from .contrib import quest_handler
from users.contrib.user_handler import isShipper, getShippers, getQuestrDetails
from .forms import QuestCreationForm, QuestChangeForm, QuestConfirmForm, QuestConfirmChangeForm
from .models import Quests

import logging

@login_required
def listallquests(request):
    # pagetype="loggedin"
    # user = request.user
    # allquests = Quests.objects.all()
    # return render(request, 'listallquest.html', locals())
    pagetitle="home"
    return redirect("home")

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

    isShipperForQuest=quest_handler.isShipperForQuest(str(user.id), questname)
    return render(request, 'viewquest.html', locals())

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

    if request.method=="POST":
        # if questdetails.questrs.id == request.user.id:
        #     instance=get_object_or_404(Quests, id=questname)
        #     user_form = QuestChangeForm(data=request.POST, instance=instance)
        #     # logging.warn(user_form.errors)
        #     # logging.warn(user_form.is_valid())
        #     if user_form.is_valid():
        #         quest_data = user_form.save(commit=False)
        #         quest_data.save()
        #         message = "Your quest has been updated!"
        #         return redirect('viewquest', questname=questname)
        from users.contrib.user_handler import getShipper
        pagetype="loggedin"
        if questdetails.questrs.id == user.id:
            instance=get_object_or_404(Quests, id=questname)
            user_form = QuestChangeForm(data=request.POST, instance=instance)
            # logging.warn(user_form.errors)
            # logging.warn(user_form.is_valid())
            # logging.warn(user_form)
            if user_form.is_valid():
                title = user_form.cleaned_data['title']
                description = user_form.cleaned_data['description']
                srccity = user_form.cleaned_data['srccity']
                srcaddress = user_form.cleaned_data['srcaddress']
                dstcity = user_form.cleaned_data['dstcity']
                dstaddress = user_form.cleaned_data['dstaddress']
                size = user_form.cleaned_data['size']
                # For distance
                #the distance and price hsa to be set up into a temp database, also the 
                #image file needs to be on a temp folder for processign to reduce API calls
                maps = geomaps.GMaps()
                origin = srcaddress+', '+srccity
                destination = dstaddress+', '+dstcity
                maps.set_geo_args(dict(origin=origin, destination=destination))
                distance = maps.get_total_distance()
                # For price
                price = pricing.WebPricing()
                price.set_factors(distance, mode=size)
                reward = price.get_price()
                pagetitle = "Confirm your Quest"
                return render(request, 'confirmquestedit.html', locals())  
        pagetitle="Edit - " + questdetails.title
        return render(request, 'editquest.html', locals())  

    # Check if the owner and the user are the same
    if questdetails.questrs.id == user.id:
        pagetitle="Edit - " + questdetails.title
        return render(request, 'editquest.html', locals())

    raise Http404
    return render(request,'404.html')

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
        #     # logging.warn(user_form.errors)
        #     # logging.warn(user_form.is_valid())
        #     if user_form.is_valid():
        #         quest_data = user_form.save(commit=False)
        #         quest_data.save()
        #         message = "Your quest has been updated!"
        #         return redirect('viewquest', questname=questname)
        from users.contrib.user_handler import getShipper
        pagetype="loggedin"
        if questdetails.questrs.id == user.id:
            instance=get_object_or_404(Quests, id=questname)
            user_form = QuestConfirmChangeForm(data=request.POST, instance=instance)
            # logging.warn(user_form.errors)
            # logging.warn(user_form.is_valid())
            # logging.warn(user_form)
            if user_form.is_valid():
                quest_data = user_form.save(commit=False)
                quest_data.save()
                pagetitle = "Confirm your Quest"
                return redirect(viewquest, questname=questdetails.id)
        pagetitle="Edit - " + questdetails.title
        return render(request, 'editquest.html', locals())  

    # Check if the owner and the user are the same
    if questdetails.questrs.id == user.id:
        pagetitle="Edit - " + questdetails.title
        return render(request, 'confirmeditquest.html', locals())

    raise Http404
    return render(request,'404.html')


@login_required
def newquest(request):
    """creates new quest and sends notification to shippers"""
    from users.contrib.user_handler import getShipper
    pagetype="loggedin"
    user = request.user

    if request.method=="POST":
        now = timezone.now()
        user_form = QuestCreationForm(request.POST)
        # logging.warn(user_form.errors)
        # logging.warn(user_form.is_valid())
        # logging.warn(user_form)
        if user_form.is_valid():
            title = user_form.cleaned_data['title']
            description = user_form.cleaned_data['description']
            srccity = user_form.cleaned_data['srccity']
            srcaddress = user_form.cleaned_data['srcaddress']
            dstcity = user_form.cleaned_data['dstcity']
            dstaddress = user_form.cleaned_data['dstaddress']
            size = user_form.cleaned_data['size']
            # For distance
            #the distance and price hsa to be set up into a temp database, also the 
            #image file needs to be on a temp folder for processign to reduce API calls
            maps = geomaps.GMaps()
            origin = srcaddress+', '+srccity
            destination = dstaddress+', '+dstcity
            maps.set_geo_args(dict(origin=origin, destination=destination))
            distance = maps.get_total_distance()
            # For price
            price = pricing.WebPricing()
            price.set_factors(distance, mode=size)
            reward = price.get_price()
            pagetitle = "Confirm your Quest"
            return render(request, 'confirmquest.html', locals())  
        if user_form.errors:
            logging.warn("Form has errors, %s ", user_form.errors)
    pagetitle = "Confirm your Quest"
    return render(request, 'newquest.html', locals())  

@login_required
def confirmquest(request):
    """creates new quest and sends notification to shippers"""
    from users.contrib.user_handler import getShipper
    pagetype="loggedin"
    user = request.user

    if request.method=="POST":
        now = timezone.now()
        user_form = QuestConfirmForm(request.POST, request.FILES)
        # logging.warn(user_form.errors)
        # logging.warn(user_form)
        # logging.warn(user_form.is_valid())
        if user_form.is_valid():
            quest_data = user_form.save(commit=False)
            quest_data.questrs_id=request.user.id
            quest_data.creation_date=now
            quest_data.item_images = user_form.cleaned_data['item_images']
            quest_data.save()
            try:
                shippers = getShippers()
                for shipper in shippers: # send notifcations to all the shippers
                    email_details = quest_handler.prepNewQuestNotification(shipper, quest_data)
                    email_notifier.send_email_notification(shipper, email_details)
            except Exception, e:
                logging.warn(e)
                pass
            quest_handler.update_resized_image(quest_data.id)
            message="Your quest has been created!"
            logging.warn(message)
            return redirect('home')
    pagetitle = "Create a Quest"
    return redirect('home')

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
    logging.warn(message)
    return redirect('viewquest', questname=questname)

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
    logging.warn(message)
    return redirect('viewquest', questname=questname)

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
                logging.debug("Quest not found")
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
                    logging.debug("Provided delivery code \'%s\' doesn't match the one in the quest number %s", delivery_code, questdetails.id)
                    logging.debug("returned to viewquest page of %s", questname)
                    return redirect('viewquest', questname=questname) # return with message
                else:
                    questr = getQuestrDetails(questdetails.questrs_id)
                    Quests.objects.filter(id=questname).update(status='Completed')
                    Quests.objects.filter(id=questname).update(is_complete='t')
                    ## Send notification to shipper
                    questr_review_link = quest_handler.get_review_link(questname, questr.id)
                    email_details = quest_handler.prepQuestCompleteNotification(shipper, questr, questdetails, questr_review_link)
                    email_notifier.send_email_notification(shipper, email_details)
                    logging.warn("Quest completion email has been sent to %s", shipper.email)
                    ## Send notification to questr
                    shipper_review_link = quest_handler.get_review_link(questname, shipper.id)
                    email_details = quest_handler.prepQuestCompleteNotification(questr, questr, questdetails, shipper_review_link)
                    email_notifier.send_email_notification(questr, email_details)
                    logging.warn("Quest completion email has been sent to %s", questr.email)
                    message="Quest completion mail has been sent to the Offerer."
                    return redirect('viewquest', questname=questname) # display message

            return redirect('viewquest', questname=questname)
        else:
            message = "Imposter detected" # Correct message required
            logging.debug(message)
            return redirect('viewquest', questname=questname)
    return redirect('viewquest', questname=questname)