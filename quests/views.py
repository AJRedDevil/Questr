from django.shortcuts import render, redirect
from django.utils import timezone
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
        # logging.warn(user_form.errors)
        # logging.warn(user_form.is_valid())
        if user_form.is_valid():
            quest_data = user_form.save(commit=False)
            # logging.warn(dir(user_form))
            quest_data.questrs_id=request.user.id
            quest_data.location="Toronto"
            quest_data.creation_date=now
            quest_data.pretty_url="jumpingjack"
            logging.warn(quest_data.reward)
            quest_data.save()
            return redirect('home')

    return render(request, 'newquest.html', locals())  

def listfeaturedquests():
    allquests = Quests.objects.all()
    return allquests

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
    return render(request, 'editquest.html', locals())  