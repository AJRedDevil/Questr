

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import render, redirect
from .models import QuestrUserProfile, UserTransactional, QuestrToken
from .forms import QuestrUserChangeForm, QuestrUserCreationForm, QuestrLocalAuthenticationForm, QuestrSocialSignupForm, CreatePasswordForm
import logging

from  access.requires import verified, is_alive
from contrib import mailing


# Create your views here.
def logout(request):
    """Logs out user"""
    auth_logout(request)
    # nextlink="signup"
    return redirect('index')
    
def login(request):
    """Home view, displays login mechanism"""
    nextlink="signup"
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == "POST":   
        auth_form = QuestrLocalAuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            auth_login(request, auth_form.get_user())
            return redirect('home')
    return render(request, 'login.html', locals())

def signup(request):
    """Signup, if request == POST, creates the user"""
    nextlink="login"
    if request.method == "POST":
        nextlink="login"
        user_form = QuestrUserCreationForm(request.POST)
        if user_form.is_valid():
            userdata = user_form.save()
            authenticate(username=userdata.email, password=userdata.password)
            userdata.backend='django.contrib.auth.backends.ModelBackend'
            auth_login(request, userdata)
            send_verfication_mail(userdata)
            return redirect('home')
        return render(request, 'signup.html', locals())
    else:
        user_form = QuestrUserCreationForm()
        return render(request, 'signup.html', locals())


def __get_verification_url(user=None): 
    """
        Returns the verification url.
    """
    verf_link = ""
    if user:
        transcational = UserTransactional(id=user.id, email=user.email)
        transcational.save()
        token_id = transcational.get_token_id()
        questr_token = QuestrToken(token_id=token_id)
        questr_token.save()
        verf_link = "{0}/user/email/confirm/{1}?questr_token={2}".format(settings.QUESTR_URL , transcational.get_truncated_user_code(), token_id)
    return verf_link

def send_verfication_mail(user):
    """
        Sends the verification email to the user
    """
    verf_link = __get_verification_url(user)
    mailing.send_verification_email(user, verf_link)

@login_required
def resend_verification_email(request):
    """
        Sends a email verification link to the corresponding email address
    """
    if request.user.is_authenticated():
        user_email = request.user
        try:
            user = QuestrUserProfile.objects.get(email=user_email)
            if user and not user.email_status:
                send_verfication_mail(user)
        except QuestrUserProfile.DoesNotExist:
            return redirect('home')
    return redirect('home')

@login_required
@verified
def home(request):
    """Post login this is returned and displays user's home page"""
    nextlink="settings"
    return render(request,'user/homepage.html', locals())

@login_required
def profile(request):
    """This displays user's profile page"""
    user = request.user
    displayname = user.displayname
    lname = user.last_name
    fname = user.first_name
    email = user.email
    biography = user.biography
    email_verified = isEmailVerified(user.email_status)
    is_active = isActive(user.is_active)
    account_status = getAccountStatus(user.account_status)
    last_online = user.last_login
    user_since = user.date_joined
    avatar = user.avatar_file_name
    password = passwordExists(request.user)
    return render(request,'user/profile.html', locals())

def getAccountStatus(status_id):
    '''Get account status of user'''
    status_list = ["Normal","Starred","Warned","Suspended","Closed"]
    if status_id < len(status_list):
        return status_list[status_id]

def isActive(status):
    """Returns if the account is active for the user"""
    return "Yes" if status else "No"

def isEmailVerified(status):
    """Returns if the email of the user has been verified"""
    return "Yes" if status else "No"

def userExists(user):
    """Checks if the user by the provided displayname exists already"""
    try:
        user = QuestrUserProfile.objects.get(displayname=user)
    except QuestrUserProfile.DoesNotExist:
        return False
    if user:
        return True

def passwordExists(user):
    """Checks if the user has created a password for himself, passwords created by PSA are unusable"""
    return user.has_usable_password()
        
def emailExists(email):
    """Checks if the user with the provided email exists already"""
    try:
        user = QuestrUserProfile.objects.get(email=email)
    except QuestrUserProfile.DoesNotExist:
        return False
    if user:
        return True

@login_required
def getUserInfo(request, displayname):
    '''This is used to display user's public profile'''
    try:
        user = QuestrUserProfile.objects.get(displayname=displayname)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'error_pages/404.html')
    else:
        lname = user.last_name
        fname = user.first_name
        if not user.privacy:            
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
    """Change's user's personal settings"""
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

@login_required
def createPassword(request):
    """Create the user's password"""
    if passwordExists(request.user):
        return redirect('home')
    if request.method == "POST":
        try:
            user_form = CreatePasswordForm(request.POST, instance=request.user)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'error_pages/404.html', locals())        
        if user_form.is_valid():
            user_form.save()
            return redirect('home')
    message="Create Password"
    return render(request, "change_passwd.html", locals())

def saveUserInfo(request):
    """This save's additional user info post the social login is successfull"""
    user_data = request.session.get('details')
    if request.method == "POST":
        user_form = QuestrSocialSignupForm(request.POST)
        if user_form.is_valid():
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['email'] = request.POST['email']
            request.session['displayname'] = request.POST['displayname']        
            backend = request.session['partial_pipeline']['backend']
            return redirect('social:complete', backend=backend)
        return render(request, "user/edituserinfo.html",locals())
    else:
        return render(request, "user/edituserinfo.html",locals())

@is_alive
def verify_email(request, user_code):
    """
        Verifies email of the user and redirect to the home page
    """
    if user_code:
        try:
            transcational = UserTransactional.objects.get(user_code__regex=r'^%s' % user_code)
            if transcational and not transcational.status:
                try:
                    user = QuestrUserProfile.objects.get(id=transcational.id)
                    if user:
                        user.email_status = True
                        user.save()
                        transcational.status = True
                        transcational.save()
                except User.DoesNotExist:
                    return redirect('home')
        except UserTransactional.DoesNotExist:
            return redirect('home')
    return redirect('home')

