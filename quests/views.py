from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .forms import QuestCreationForm
from .models import Quests

import logging

# Create your views here.
@login_required
def createquest(request):
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
        logging.warn(user_form.errors)
        logging.warn(user_form.is_valid())
        if user_form.is_valid():
            quest_data = user_form.save(commit=False)
            quest_data.questrs_id=request.user.id
            quest_data.creation_date=now
            quest_data.save()
            return redirect('home')

    return render(request, 'newquest.html', locals())  

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
    secondnav="listquestsecondnav"
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

    # Check if the owner and the user are the same
    if questdetails.questrs.id == request.user.id:
        return render(request, 'editquest.html', locals())

    raise Http404
    return render(request,'404.html')