from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import Http404
from .models import QuestrUserProfile
from .forms import QuestrUserProfileForm

# Create your views here.
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('index')
    
def login(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('home')
    return render(request, 'user/signup.html', locals())

@login_required
def home(request):
    """Post login this is returned and displays user's home page"""
    return render(request,'user/homepage.html', locals())

@login_required
def profile(request):
    """Post login this is returned and displays user's home page"""
    user = request.user
    lname = user.last_name
    fname = user.first_name
    email = user.email
    bio = user.biography
    email_verified = isEmailVerified(user.email_status)
    is_active = isActive(user.is_active)
    account_status = getAccountStatus(user.account_status)
    last_online = user.last_login
    user_since = user.date_joined
    avatar = user.avatar_file_name
    return render(request,'user/profile.html', locals())

@login_required
def settings(request):
    pass

def getAccountStatus(status_id):
    '''Get account status of user'''
    status_list = ["Normal","Starred","Warned","Suspended","Closed"]
    if status_id < len(status_list):
        return status_list[status_id]

def isActive(status):
    return "Yes" if status else "No"

def isEmailVerified(status):
    return "Yes" if status else "No"

@login_required
def getUserInfo(request, username):
    '''This is used to display user's public profile'''
    try:
        user = QuestrUserProfile.objects.get(username=username)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'error_pages/404.html')
    else:
        lname = user.last_name
        fname = user.first_name
        if not user.privacyToggle:            
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

@login_required
def editUserInfo(request):
    if request.method == "POST":
        try:
            user_form = QuestrUserProfileForm(request.POST, instance=request.user)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'error_pages/404.html', locals())        
        if user_form.is_valid():
            user_form.save()
            messageresponse = "Your profile has been upated"
            return render(request, "user/edituserinfo.html",locals())
    else:
        try:
            user_form = QuestrUserProfileForm(instance=request.user)
            return render(request, "user/edituserinfo.html",locals())
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'error_pages/404.html', locals())
    return render(request, "user/edituserinfo.html",locals())





