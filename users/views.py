

import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import render, redirect
from .models import QuestrUserProfile, UserTransactional, QuestrToken
from .forms import QuestrUserChangeForm, QuestrUserCreationForm, QuestrLocalAuthenticationForm, QuestrSocialSignupForm, SetPasswordForm, PasswordChangeForm

from libs import email_notifier

from access.requires import verified, is_alive
from contrib import mailing, user_handler

from quests.contrib import quest_handler
from quests.models import Quests
from reviews.models import Review
from reviews.contrib import review_handler

# Create your views here.
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('index')
    
def login(request):
    """Home view, displays login mechanism"""
    pagetype="public"
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == "POST":   
        auth_form = QuestrLocalAuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            auth_login(request, auth_form.get_user())
            return redirect('home')
    pagetitle = "Login"
    return render(request, 'signin.html', locals())

def signup(request):
    """Signup, if request == POST, creates the user"""
    pagetype="public"
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == "POST":
        user_form = QuestrUserCreationForm(request.POST)
        logging.warn(user_form.is_valid())
        logging.warn(user_form.errors)
        if user_form.is_valid():
            userdata = user_form.save()
            authenticate(username=userdata.email, password=userdata.password)
            userdata.backend='django.contrib.auth.backends.ModelBackend'
            auth_login(request, userdata)
            user_handler.send_verfication_mail(userdata)
            pagetitle = "Please verify your email !"
            return render(request, 'thankyou.html', locals())
        pagetitle = "Signup"
        return render(request, 'signup.html', locals())
    else:
        user_form = QuestrUserCreationForm()
        pagetitle = "Signup"
        return render(request, 'signup.html', locals())

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
                user_handler.send_verfication_mail(user)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'404.html')
    return redirect('home')

@login_required
@verified
def home(request):
    """Post login this is returned and displays user's home page"""
    pagetype="loggedin"
    secondnav="listquestsecondnav"
    user = request.user
    allquests = Quests.objects.filter(ishidden=False)
    # logging.warn(allquests)
    pagetitle = "Home"
    return render(request,'homepage.html', locals())

@login_required
def profile(request):
    """This displays user's profile page"""
    pagetype="loggedin"
    user = request.user
    try:
        user = QuestrUserProfile.objects.get(email=request.user)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    try:
        questsbyuser = quest_handler.getQuestsByUser(user.id)
    except Exception, e:
        raise e
        return render(request,'broke.html')

    try:
        final_rating = Review.objects.filter(reviewed=user).aggregate(Avg('final_rating'))
    except Review.DoesNotExist:
        final_rating['final_rating__avg'] = 0.0
    # for users without rating
    if not final_rating['final_rating__avg']:
            final_rating['final_rating__avg'] = 0.0

    final_rating = round(final_rating['final_rating__avg'], 1)

    try:
        allreviews = review_handler.get_review(user.id)
    except Exception, e:
        raise e
        return render(request,'broke.html')
    pagetitle = user.first_name+' '+user.last_name
    return render(request,'profile.html', locals())

@login_required
def userSettings(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    settingstype="general"
    password = user_handler.passwordExists(user)
    try:
        user = QuestrUserProfile.objects.get(email=request.user)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'404.html', locals())

    if request.method == "POST":
        try:
            user_form = QuestrUserChangeForm(request.POST, instance=request.user)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'404.html', locals())        
        if user_form.is_valid():
            user_form.save()
            message="Your profile has been updated!"
            return redirect('settings')
    pagetitle = "My Settings"
    return render(request, "generalsettings.html",locals())

@login_required
def myTrades(request):
    # pagetype="loggedin"
    # user = request.user
    # pagetitle = "My Trades"
    # shipperlist = {} #init blank dict
    
    # questswithoffers = quest_handler.getQuestsWithOffer(user.id) # list of the logged in user's quest where offers are put

    # for quest in questswithoffers:
    #     shippers = user_handler.getShippersOfQuest(quest.id) # for each quest get the individual shippers
    #     shipper_object_list = []
    #     for shipper_id in shippers:
    #         # build a dict of quest and shipper objects
    #         shipper_object_list.append(user_handler.getShipper(shipper_id) )
        
    #     shipperlist[quest]=shipper_object_list
    
    # # logging.warn(shipperlist)
    # return render(request, 'trades.html', locals())
    return redirect('myposts')

@login_required
def acceptOffer(request, quest_id, shipper_id):
    """Accepts a bid on a quest from a user"""
    pagetype="loggedin"
    user = request.user
    # if the shipper doesn't exist
    if not user_handler.userExists(shipper_id):
        logging.warn("User ID : %s not found, quest %s not accepted, returning to mytrades page", shipper_id, quest_id)
        return redirect('mytrades')    
    
    try:
        Quests.objects.filter(id=quest_id).update(shipper=shipper_id, isaccepted='t')
        Quests.objects.filter(id=quest_id).update(status='Accepted')
        questdetails = quest_handler.getQuestDetails(quest_id)
        shipper = user_handler.getQuestrDetails(shipper_id)
        email_details = quest_handler.prepOfferAcceptedNotification(shipper, questdetails)
        email_notifier.send_email_notification(shipper, email_details)
    except Quests.DoesNotExist:
        raise Http404
        return render('404.html', locals())
    #To display the information of shipper on the trades page
    shipper = user_handler.getShipper(shipper_id)    
    
    return redirect('mytrades')

@login_required
def myPosts(request):
    pagetype="loggedin"
    user = request.user
    pagetitle = "My Trades"
    shipperlist = {} #init blank dict
    
    questswithoffers = quest_handler.getQuestsWithOffer(user.id) # list of the logged in user's quest where offers are put
    questswithoutoffers = quest_handler.getQuestsByUser(user.id) # list of the logged in user's quest where offers aren't put

    for quest in questswithoffers:
        shippers = user_handler.getShippersOfQuest(quest.id) # for each quest get the individual shippers
        shipper_object_list = []
        for shipper_id in shippers:
            # build a dict of quest and shipper objects
            shipper_object_list.append(user_handler.getShipper(shipper_id) )
        
        shipperlist[quest]=shipper_object_list
    
    # logging.warn(shipperlist)
    return render(request, 'myquests.html', locals())

@login_required
def myShipments(request):
    pagetype="loggedin"
    user = request.user
    pagetitle = "My Shipments"
    myshipments = quest_handler.getMyShipmnets(user.id)
    return render(request, 'myshipments.html', locals())

@login_required
def getUserInfo(request, displayname):
    '''This is used to display user's public profile'''
    pagetype="loggedin"
    user = request.user
    try:
        publicuser = QuestrUserProfile.objects.get(displayname=displayname)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render(request,'404.html')

    try:
        questsbyuser = quest_handler.getQuestsByUser(publicuser.id)
    except Exception, e:
        raise e
        return render(request,'broke.html')

    try:
        allreviews = review_handler.get_review(publicuser.id)
    except Exception, e:
        raise e
        return render(request,'broke.html')

    try:
        final_rating = Review.objects.filter(reviewed=publicuser).aggregate(Avg('final_rating'))
    except Review.DoesNotExist:
        final_rating['final_rating__avg'] = 0.0
    # for users without rating
    if not final_rating['final_rating__avg']:
            final_rating['final_rating__avg'] = 0.0

    final_rating = round(final_rating['final_rating__avg'], 1)

    pagetitle = publicuser.first_name+' '+publicuser.last_name
    return render(request,'publicprofile.html', locals())

@login_required
def createPassword(request):
    """Create a password for socially logged in user"""
    pagetype="loggedin"
    user = request.user
    settingstype="password"

    if user_handler.passwordExists(request.user):
        return redirect('home')
    
    if request.method == "POST":
        user_form = SetPasswordForm(user, request.POST)
        if user_form.is_valid():
            user_form.save()
            message="Your password has been created!"
            return redirect('home')
    pagetitle = "Create Your Password"
    return render(request, "createpassword.html", locals())

@login_required
def changePassword(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    settingstype="password"
    ##check if the user has password, if they don't they'd be provided with a link to create one for them
    password = user_handler.passwordExists(user)
    # logging.warn(user)
    # logging.warn(password)

    if request.method == "POST":
        user_form = PasswordChangeForm(user, request.POST)
        logging.warn(user_form.errors)
        if user_form.is_valid():
            user_form.save()
            message="Your password has been changed!"
            return redirect('changepassword')
    pagetitle = "Change Your Password"
    return render(request, "passwordsettings.html",locals())

@login_required
def cardSettings(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    settingstype="card"
    return render(request, "cardsettings.html",locals())

@login_required
def emailSettings(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    settingstype="email"
    return render(request, "emailsettings.html",locals())

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
        return render(request, "socialsignup.html",locals())
    else:
        return render(request, "socialsignup.html",locals())

@is_alive
def verify_email(request, user_code):
    """
        Verifies email of the user and redirect to the home page
    """
    logging.warn(user_code)
    if user_code:
        try:
            transcational = UserTransactional.objects.get(user_code__regex=r'^%s' % user_code)
            logging.debug("transactional")
            logging.debug(transcational)
            if transcational:
                logging.debug("transctional status")
                logging.warn(transcational.status)
                if not transcational.status:
                    try:
                        user = QuestrUserProfile.objects.get(email=transcational.email)
                        logging.warn(user)
                        if user:
                            user.email_status = True
                            user.save()
                            transcational.status = True
                            transcational.save()
                    except QuestrUserProfile.DoesNotExist:
                        logging.debug('User does not exist')
                        return redirect('home')
                else:
                    message = "Please use the latest verification email sent."
                    return redirect('home', locals())
        except UserTransactional.DoesNotExist:
            return redirect('home')
    return redirect('home')

def resetpassword(request):
    """
    Mail new random password to the user.
    """
    if request.method=="POST":
        user_email = request.POST['email']
        try:
            user = QuestrUserProfile.objects.get(email = user_email)
        except Exception, e:
            message ="Bruh, a user with that email doesnt exist!"
            return render(request, "resetpassword.html", locals())
        if user:
            new_random_password = user_handler.get_random_password()
            user.set_password(new_random_password)
            user.save()
            mailing.send_reset_password_email(user, new_random_password)
            message = "Please check your inbox for your new password"
            return render(request, "homepage.html", locals())
    pagetitle = "Reset Your Password"
    pagetype  = "public"
    return render(request,"resetpassword.html", locals())
