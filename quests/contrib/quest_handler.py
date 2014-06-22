

from django.shortcuts import render, redirect
from django.conf import settings

from quests.models import Quests

import logging
# Create your views here.
def listfeaturedquests(questrs_id):
    """List all the featured quests"""
    allquests = Quests.objects.exclude(questrs_id=questrs_id)
    return allquests

def getQuestsByUser(questrs_id):
    """List all the quests by a particular user"""
    try:
        questsbysuer = Quests.objects.filter(questrs_id=questrs_id)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    return questsbysuer

def getQuestsWithOffer(questrs_id):
    """Lists a user's quest where offers are put"""
    try:
        questsWithOffer = Quests.objects.filter(questrs_id=questrs_id).exclude(shipper=None)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')
    return questsWithOffer

def isShipperForQuest(shipper_id, questname):
    """Returns if the current shipper is listed in for the quest"""
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    current_shipper = questdetails.shipper
    if current_shipper != None:
        if shipper_id in current_shipper:
            return True
        return False
    return False

def addShipper(shipper_id, questname):
    """adds a shipper to a posted quest"""
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    current_shipper = questdetails.shipper
    # for first application
    logging.warn(current_shipper)
    if current_shipper==None:
        current_shipper = []
    else:
        current_shipper = current_shipper.split(',')
    # check if shipper has already applied
    if not shipper_id in current_shipper:
        current_shipper.append(shipper_id)
        current_shipper = ','.join(current_shipper)
    else:
        return redirect('home')

    try:
        Quests.objects.filter(id=questname).update(shipper=current_shipper)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

def delShipper(shipper_id, questname):
    """adds a shipper to a posted quest"""
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    current_shipper = questdetails.shipper
    if current_shipper==None:
        #If no user has bid so far , redirect to home
        return redirect('home')
    else:
        current_shipper = current_shipper.split(',')
    # check if shipper has already applied
    if shipper_id in current_shipper:
        current_shipper.remove(shipper_id)
        if current_shipper:
            current_shipper = ','.join(current_shipper)
        else:
            current_shipper=None
    else:
        return redirect('home')

    try:
        Quests.objects.filter(id=questname).update(shipper=current_shipper)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

def prepNewQuestNotification(user, questdetails):
    """Prepare the details for notification emails for new quests"""
    template_name="New_Quest_Notification"
    subject="New Quest Notification"
    # quest_browse_link=settings.QUESTR_URL+"/quest"
    quest_support_email="support@questr.co"
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'quest_public_link' : settings.QUESTR_URL+'/quest/'+str(questdetails.id),
                                                'quest_description' : questdetails.description,
                                                'user_first_name'   : user.first_name,
                                                'email_unsub_link'  : questr_unsubscription_link,
                                                'quest_title'       : questdetails.title,
                                                'quest_reward'      : str(questdetails.reward),
                                                'quest_support_mail': quest_support_email,
                                                'recipient_id'      : user.id,
                                                'questr_unsubscription_link' : questr_unsubscription_link,
                                                'company'           : "Questr Co"

                                                },
                    }
    return email_details