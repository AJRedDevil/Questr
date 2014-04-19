from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import Http404
from .models import QuestrUserProfile
from .forms import QuestrUserChangeForm, QuestrUserCreationForm


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

def signup(request):
    """Signup, if request == POST, creates the user"""
    if request.method == "POST":
        user_form = QuestrUserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.check_password_match()
            userdata = user_form.save()
            authenticate(username=userdata.username, password=userdata.password)
            userdata.backend='django.contrib.auth.backends.ModelBackend'
            auth_login(request, userdata)
            return redirect('home')
        return render(request, 'signup.html', locals())
    else:
        return render(request, 'signup.html', locals())

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
        if not user.privacytoggle:            
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
            user_form = QuestrUserChangeForm(request.POST, instance=request.user)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'error_pages/404.html', locals())        
        if user_form.is_valid():
            user_form.save()
            messageresponse = "Your profile has been upated"
            return render(request, "user/edituserinfo.html",locals())
    else:
        try:
            user_form = QuestrUserChangeForm(instance=request.user)
            return render(request, "user/edituserinfo.html",locals())
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'error_pages/404.html', locals())
    return render(request, "user/edituserinfo.html",locals())

def saveUserInfo(request):
    user_data = request.session.get('details')
    if request.method == "POST":
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        request.session['username'] = request.POST.get('username')
        request.session['email'] = request.POST.get('email')
        request.session['biography'] = request.POST.get('bio')
        request.session['phone'] = request.POST.get('phone')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    else:
        return render(request, "user/edituserinfo.html",locals())





