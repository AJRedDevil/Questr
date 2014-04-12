from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import Http404
from .models import QuestrUserProfile

# Create your views here.
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('index')
    
def login(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('profile')
    return render(request, 'user/signup.html', locals())

@login_required
def profile(request):
    """Login complete view, displays user data"""
    user = request.user
    return render(request,'user/profile.html', locals())

@login_required
def settings(request):
    pass

def getAccountStatus(status_id):
    status_list = ["Normal","Starred","Warned","Suspended","Closed"]
    if status_id < len(status_list):
        return status_list[status_id]

def isActive(status):
    return "Yes" if status else "No"

def isEmailVerified(status):
    return "Yes" if status else "No"

def getUserInfo(request, username):
    # from projects import getInvolvedProjects,getAdminProjects
    try:
        user = QuestrUserProfile.objects.get(username=username)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'error_pages/404.html')
    else:
        lname = user.last_name
        fname = user.first_name
        if user.privacyToggle:            
            email = user.email
        bio = user.biography
        email_verified = isEmailVerified(user.email_status)
        is_active = isActive(user.is_active)
        account_status = getAccountStatus(user.account_status)
        last_online = user.last_login
        user_since = user.date_joined
        avatar = user.avatar_file_name
        # questsOpened = getQuestsOpened(user)
        # offersPlaced = getOffersPlaced(user)
    return render(request,'user/userinfo.html', locals())




