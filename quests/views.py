from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.decorators import login_required

from libs import email_notifier

from .forms import QuestCreationForm, QuestChangeForm
from .models import Quests

import logging

# Create your views here.
def listfeaturedquests():
    """List all the featured quests"""
    allquests = Quests.objects.all()
    return allquests

def getQuestsByUser(questrs_id):
    """List all the quests by a particular user"""
    questsbysuer = Quests.objects.filter(questrs_id=questrs_id)
    return questsbysuer

@login_required
def listallquests(request):
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    allquests = Quests.objects.all()
    return render(request, 'listallquest.html', locals())

@login_required
def viewquest(request, questname):
    pagetype="loggedin"
    user = request.user
    questname=questname
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        isOwner = True
    return render(request, 'viewquest.html', locals())

@login_required
def editquest(request, questname):
    pagetype="loggedin"
    user = request.user
    questname=questname
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    try:
        questdetails = Quests.objects.get(id=questname)
    except Quests.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    if request.method=="POST":
        if questdetails.questrs.id == request.user.id:
            instance=get_object_or_404(Quests, id=questname)
            user_form = QuestChangeForm(data=request.POST, instance=instance)
            # logging.warn(user_form.errors)
            # logging.warn(user_form.is_valid())
            if user_form.is_valid():
                quest_data = user_form.save(commit=False)
                quest_data.save()
                return redirect('home')

    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        return render(request, 'editquest.html', locals())

    raise Http404
    return render(request,'404.html')

def prepNewQuestNotification(user, questdetails):
    """Prepare the details for notification emails for new quests"""
    template_name="New_Quest_Notification"
    subject="New Quest Notification"
    quest_browse_link="http://questr.co/quest"
    quest_support_email="support@questr.co"
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'quest_public_link' : "http://questr.co/quest/"+str(questdetails.id),
                                                'quest_description' : questdetails.description,
                                                'user_first_name'   : user.first_name,
                                                'email_unsub_link'  : questr_unsubscription_link,
                                                'quest_title'       : questdetails.title,
                                                'quest_reward'      : str(questdetails.reward),
                                                'quest_browse_link' : quest_browse_link,
                                                'quest_support_mail': quest_support_email,
                                                'recipient_id'      : user.id,
                                                'questr_unsubscription_link' : questr_unsubscription_link,
                                                'company'           : "Questr Co"

                                                },
                    }
    return email_details

@login_required
def createquest(request):
    from users.views import getUsersWitNotificationEnabled
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"

    if request.method=="POST":
        now = timezone.now()
        user_form = QuestCreationForm(data=request.POST)
        # logging.warn(user_form.errors)
        # logging.warn(user_form.is_valid())
        if user_form.is_valid():
            quest_data = user_form.save(commit=False)
            quest_data.questrs_id=request.user.id
            quest_data.creation_date=now
            quest_data.save()
            try:
                usersToBeNotified = getUsersWitNotificationEnabled()
                for users in usersToBeNotified:
                    email_details = prepNewQuestNotification(users, quest_data)
                    email_notifier.send_newquest_notification(users, email_details)
            except Exception, e:
                logging.warn(e)
                pass
            return redirect('home')

    return render(request, 'newquest.html', locals())  
