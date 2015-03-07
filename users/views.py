

#All Djang Imports
# from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

#All local imports (libs, contribs, models)
from access.requires import verified, is_alive, is_superuser, is_signup_token_alive
from contrib import user_handler
from libs import email_notifier, pricing
from quests.contrib import quest_handler
from quests.models import Quests
from reviews.contrib import review_handler
from reviews.models import Review
from .models import QuestrUserProfile, UserToken
from .forms import QuestrUserChangeForm, QuestrUserCreationForm, QuestrLocalAuthenticationForm, \
PasswordChangeForm, NotifPrefForm, SignupInvitationForm, SetPasswordForm

#All external imports (libs, packages)
from ipware.ip import get_real_ip, get_ip
import simplejson as json
import logging


# Init Logger
logger = logging.getLogger(__name__)


# Create your views here.
def logout(request):
    """Logs out user"""
    user = user_handler.getQuestrDetails(request.user.id)
    auth_logout(request)
    eventhandler = user_handler.UserEventManager()
    extrainfo = dict()
    eventhandler.setevent(user, 0, extrainfo)
    return redirect('index')
    
def signin(request):
    """
    Home view, displays login mechanism
    """
    # if authenticated redirect to user's homepage directly
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    # for redirects to signin
    if request.GET:  
        next = request.GET['next']

    # for users already signed in
    if request.user.is_authenticated():
        return redirect('home')

    if request.method == "POST":   
        auth_form = QuestrLocalAuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            auth_login(request, auth_form.get_user())
            eventhandler = user_handler.UserEventManager()
            extrainfo = dict(client_public_ip=client_public_ip, client_internal_ip=client_internal_ip)
            eventhandler.setevent(request.user, 1, extrainfo)
            # Notify the user of his status if he's unavailable
            if request.user.is_authenticated() and request.user.is_shipper and request.user.is_available == False:
                    request.session['alert_message'] = dict(type="warning",message="Your status is set to unavailable, you might want to set it to available!")
                    if request.POST.get('next'):
                        return HttpResponseRedirect(request.POST.get('next'))
                    return redirect('home')
            return redirect('home')

        if auth_form.errors:
            logger.debug("Login Form has errors, %s ", auth_form.errors)
    pagetitle = "Login"
    return render(request, 'signin.html', locals())

def signup(request):
    """Signup, if request == POST, creates the user"""
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == "POST":
        user_form = QuestrUserCreationForm(request.POST)
        if user_form.is_valid():
            useraddress = dict(city=user_form.cleaned_data['city'], streetaddress=user_form.cleaned_data['streetaddress'],\
                postalcode=user_form.cleaned_data['postalcode'])
            logging.warn(useraddress)
            userdata = user_form.save(commit=False)
            userdata.address = json.dumps(useraddress)
            userdata.phone = user_form.cleaned_data['phone']
            userdata.save()
            authenticate(username=userdata.email, password=userdata.password)
            userdata.backend='django.contrib.auth.backends.ModelBackend'
            auth_login(request, userdata)
            verf_link = user_handler.get_verification_url(userdata)
            logger.debug("verification link is %s", verf_link)
            email_details = user_handler.prepWelcomeNotification(userdata, verf_link)
            logger.debug("What goes in the email is \n %s", email_details)
            email_notifier.send_email_notification(userdata, email_details)
            pagetitle = "Please verify your email !"
            return redirect('home')

        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
        pagetitle = "Signup"
        return render(request, 'signup.html', locals())
    else:
        user_form = QuestrUserCreationForm()
        pagetitle = "Signup"
        return render(request, 'signup.html', locals())

@login_required
@is_superuser
def createcourier(request):
    """Signup, if request == POST, creates the user"""
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        user = request.user
        pagetype="loggedin"

    if request.method == "POST":
        user_form = QuestrUserCreationForm(request.POST)
        if user_form.is_valid():
            useraddress = dict(city=user_form.cleaned_data['city'], streetaddress=user_form.cleaned_data['streetaddress'],\
                streetaddress_2=user_form.cleaned_data['streetaddress_2'], postalcode=user_form.cleaned_data['postalcode'])
            userdata = user_form.save(commit=False)
            userdata.address = json.dumps(useraddress)
            userdata.email_status = True
            userdata.is_shipper = True
            userdata.phone = user_form.cleaned_data['phone']
            # import hashlib
            # import uuid
            # hashstring = hashlib.sha256(str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())).hexdigest()
            # password = hashstring[:4]+hashstring[-2:]
            password = user_form.cleaned_data['password1']
            userdata.set_password(password)
            userdata.save()
            email_details = user_handler.prepWelcomeCourierNotification(userdata, password)
            logger.debug("What goes in the email is \n %s", email_details)
            email_notifier.send_email_notification(userdata, email_details)
            request.session['alert_message'] = dict(type="success",message="Shipper has been created!")
            return redirect('home')

        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
        pagetitle = "Create a Courier"
        return render(request, 'createcourier.html', locals())
    else:
        user_form = QuestrUserCreationForm()
        pagetitle = "Create a Courier"
        return render(request, 'createcourier.html', locals())

@login_required
@is_superuser
def createuser(request):
    """Signup, if request == POST, creates the user"""
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        user = request.user
        pagetype="loggedin"

    if request.method == "POST":
        user_form = QuestrUserCreationForm(request.POST)
        if user_form.is_valid():
            useraddress = dict(city=user_form.cleaned_data['city'], streetaddress=user_form.cleaned_data['streetaddress'],\
                streetaddress_2=user_form.cleaned_data['streetaddress_2'], postalcode=user_form.cleaned_data['postalcode'])
            userdata = user_form.save(commit=False)
            userdata.address = json.dumps(useraddress)
            userdata.email_status = True
            userdata.phone = user_form.cleaned_data['phone']
            import hashlib
            import uuid
            hashstring = hashlib.sha256(str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())).hexdigest()
            password = hashstring[:4]+hashstring[-2:]
            userdata.set_password(password)
            userdata.save()
            # default_pricing = { 'rate_meter_drop_weekend' : {'car': 8, 'backpack': 6, 'truck': 90, 'minivan': 10} ,
            #                     'rate_per_km_weekend' : {'car': 1.2, 'backpack': 1.0, 'truck': 90, 'minivan': 2.2},
            #                     'rate_meter_drop_weekday' : {'car': 6, 'backpack': 5, 'truck': 90, 'minivan': 10}, 
            #                     'rate_per_km_weekday' : {'car': 1.0, 'backpack': 0.8, 'truck': 75, 'minivan': 2.0},
            #                     'hourlist' : {'off_peak_hours': {'start_min': 0, 'start_hr': 8, 'end_hr': 21, 'end_min': 59}},
            #                     'chargefreekm' : 2
            #                     }
            # pricingmodel = pricing.WebPricing(userdata)
            # pricingmodel = QuestPricing(pricing=default_pricing, questrs=userdata)
            # pricingmodel.save()

            email_details = user_handler.prepWelcomeCourierNotification(userdata, password)
            logger.debug("What goes in the email is \n %s", email_details)
            email_notifier.send_email_notification(userdata, email_details)
            request.session['alert_message'] = dict(type="success",message="User has been created!")
            return redirect('home')

        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
        pagetitle = "Create a User"
        return render(request, 'createuser.html', locals())
    else:
        user_form = QuestrUserCreationForm()
        pagetitle = "Create a User"
        return render(request, 'createuser.html', locals())

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
                verf_link = user_handler.get_verification_url(user)
                logger.debug("verification link is %s", verf_link)
                email_details = user_handler.prepWelcomeNotification(user, verf_link)
                logger.debug("What goes in the email is \n %s", email_details)
                email_notifier.send_email_notification(user, email_details)
                # user_handler.send_verfication_mail(user)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'404.html')
    request.session['alert_message'] = dict(type="success",message="The verification link has been sent to your email")
    return redirect('home')

@login_required
@verified
def home(request):
    """Post login this is returned and displays user's home page"""
    pagetype="loggedin"
    secondnav="listquestsecondnav"
    user = request.user
    userdetails = user_handler.getQuestrDetails(user.id)
    pagetitle = "Home"
    if userdetails.is_shipper:
        alert_message = request.session.get('alert_message')
        if request.session.has_key('alert_message'):
            del request.session['alert_message']
        activequests = Quests.objects.filter(ishidden=False, isaccepted=True, shipper=userdetails.id, is_complete=False).order_by('-creation_date')[:10]
        pastquests = Quests.objects.filter(ishidden=False, is_complete=True, isaccepted=True, shipper=userdetails.id).order_by('-creation_date')[:10]

        return render(request,'homepage.html', locals())
    elif userdetails.is_superuser:
        alert_message = request.session.get('alert_message')
        if request.session.has_key('alert_message'):
            del request.session['alert_message']
        allquests = Quests.objects.filter(ishidden=False, isaccepted=True, shipper=0).order_by('-creation_date')[:10]
        return render(request,'shipperhomepage.html', locals())
    else:
        alert_message = request.session.get('alert_message')        
        if request.session.has_key('alert_message'):
            del request.session['alert_message']
        allquests = Quests.objects.filter(ishidden=False, isaccepted=False, questrs_id=userdetails.id, ).order_by('-creation_date')[:10]
        activequests = Quests.objects.filter(ishidden=False, isaccepted=True, is_complete=False, questrs_id=userdetails.id).order_by('-creation_date')[:10]
        pastquests = Quests.objects.filter(ishidden=False, is_complete=True, questrs_id=userdetails.id).order_by('-creation_date')[:10]
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
        questsbyuser = quest_handler.getQuestsByUser(user)
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
    password = user_handler.passwordExists(user)
    userdetails = user_handler.getQuestrDetails(user.id)
    if request.method == "POST":
        logging.warn(request.POST)
        try:
            user_form = QuestrUserChangeForm(request.POST,request.FILES, instance=request.user)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'404.html', locals())  
        if user_form.is_valid():
            useraddress = dict(city=user_form.cleaned_data['city'], streetaddress=user_form.cleaned_data['streetaddress'],\
                streetaddress_2=user_form.cleaned_data['streetaddress_2'], postalcode=user_form.cleaned_data['postalcode'])
            if user_form.cleaned_data['email'] != userdetails.email:
                userdata = user_form.save(commit=False)
                userdata.address = json.dumps(useraddress)
                userdata.phone = user_form.cleaned_data['phone']
                userdata.email_status = False
                userdata.save()
                verf_link = user_handler.get_verification_url(userdata)
                logger.debug("verification link is %s", verf_link)
                email_details = user_handler.prepWelcomeNotification(userdata, verf_link)
                logger.debug("What goes in the email is \n %s", email_details)
                email_notifier.send_email_notification(userdata, email_details)
                pagetitle = "Please verify your email !"
                return redirect('home')
            else:
                userdata = user_form.save(commit=False)
                userdata.address = json.dumps(useraddress)
                userdata.phone = user_form.cleaned_data['phone']

            if user_form.cleaned_data['avatar'] is not None:
                userdata.avatar = user_form.cleaned_data['avatar']
            else:
                userdata.avatar = userdetails.avatar
            logger.warn("file is %s" % userdata.avatar)
            userdata.save()
            request.session['alert_message'] = dict(type="Success",message="Your profile has been updated!")
            return redirect('settings')
        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)
    alert_message = request.session.get('alert_message')
    if request.session.has_key('alert_message'):
        del request.session['alert_message']
    pagetitle = "My Settings"
    return render(request, "generalsettings.html",locals())

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
        questsbyuser = quest_handler.getQuestsByUser(publicuser)
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

@is_alive
def createpassword(request):
    """
    Create a password for socially logged in user
    """
    if request.GET['questr_token']:
        questr_token = request.GET['questr_token']
        try:
            prev_token = UserToken.objects.get(token = questr_token, token_type = 3)
            if prev_token:
                logger.debug("transctional status")
                logger.debug(prev_token.status)
                if not prev_token.status:
                    try:
                        userobj = QuestrUserProfile.objects.get(email=prev_token.email)
                        if request.method=="POST":
                            user_form = SetPasswordForm(userobj, request.POST)
                            if user_form.is_valid():
                                userdata = user_form.save()
                                prev_token.status = True
                                prev_token.save()
                                request.session['alert_message'] = dict(type="success",message="Thankyou for verifying your email! Welcome to Questr! ")
                                return redirect('home')
                            if user_form.errors:
                                logger.debug("Form has errors, %s ", user_form.errors)
                            questr_token = request.GET['questr_token']
                            pagetitle = "Reset Your Password"
                            return render(request, 'createpassword.html', locals())
                        else:
                            questr_token = request.GET['questr_token']
                            pagetitle = "Reset Your Password"
                            return render(request, 'createpassword.html', locals())
                    except QuestrUserProfile.DoesNotExist:
                        logger.debug('User does not exist')
                        return redirect('home')
                else:
                    request.session['alert_message'] = dict(type="warning",message="Please use the latest verification email sent, or click below to send a new email.")
                    return redirect('home')
        except prev_token.DoesNotExist:
            return redirect('home')
    return redirect('home')


@login_required
def changePassword(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    settingstype="password"
    ##check if the user has password, if they don't they'd be provided with a link to create one for them
    password = user_handler.passwordExists(user)
    # logger.debug(user)
    # logger.debug(password)

    if request.method == "POST":
        user_form = PasswordChangeForm(user, request.POST)
        logger.debug(user_form.errors)
        if user_form.is_valid():
            user_form.save()
            request.session['alert_message'] = dict(type="success",message="Your password has been changed successfully!")
            return redirect('logout')
    pagetitle = "Change Your Password"
    return render(request, "passwordsettings.html",locals())

@verified
@login_required
def notificationsettings(request):
    """Change's user's personal settings"""
    pagetype="loggedin"
    user = request.user
    settingstype="Notifications"
    if request.method == "POST":
        user_form = NotifPrefForm(request.POST)
        if user_form.is_valid():
            prefdict = {}
            package = user_form.cleaned_data['package']
            notif = user_form.cleaned_data['notif']
            prefdict['package'] = package
            prefdict['notif'] = notif
            QuestrUserProfile.objects.filter(id=request.user.id).update(notificationprefs=prefdict)

        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)

    user_form = NotifPrefForm()
    pagetitle = "Email Notification Settings"
    return render(request, "emailsettings.html",locals())

@is_alive
@login_required
def verify_email(request):
    """
        Verifies email of the user and redirect to the home page
    """
    if request.GET['questr_token']:
        questr_token = request.GET['questr_token']
        try:
            prev_token = UserToken.objects.get(token = questr_token)
            if prev_token:
                logger.debug("transctional status")
                logger.debug(prev_token.status)
                if not prev_token.status:
                    try:
                        user = QuestrUserProfile.objects.get(email=prev_token.email)
                        logger.debug(user)
                        if user:
                            user.email_status = True
                            user.save()
                            prev_token.status = True
                            prev_token.save()
                            request.session['alert_message'] = dict(type="success",message="Thankyou for verifying your email! Welcome to Questr! ")
                            return redirect('home')
                    except QuestrUserProfile.DoesNotExist:
                        logger.debug('User does not exist')
                        return redirect('home')
                else:
                    request.session['alert_message'] = dict(type="warning",message="Please use the latest verification email sent, or click below to send a new email.")
                    return redirect('home')
        except prev_token.DoesNotExist:
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
            reset_link = user_handler.get_password_reset_url(user.email)
            # new_random_password = user_handler.get_random_password()
            # user.set_password(new_random_password)
            # user.save()
            email_details = user_handler.prepPasswordResetNotification(user, reset_link)
            email_notifier.send_email_notification(user, email_details)
            message = "Please check your inbox for your new password"
            return redirect('signin')
    pagetitle = "Reset Your Password"
    pagetype  = "public"
    return render(request,"resetpassword.html", locals())

@verified
@login_required
def changestatus(request):
    """Changes the courier's availability from the one that he is currently on"""
    user = request.user
    if user.is_shipper and user.email_status:
        availability = user.is_available
        if availability:
            # If the user is available, change his status to unavailable
            result = user_handler.updateCourierAvailability(user, False)
        else:
            # vice versa
            result = user_handler.updateCourierAvailability(user, True)
    else:
        return redirect('home')

    if result['success'] == "True":
        request.session['alert_message'] = dict(type="Success",message="Your status has been updated!")
        return redirect("home")
    elif result['success'] == "False":
        request.session['alert_message'] = dict(type="Danger",message="Your status cannot be updated!")
        return redirect("home")

@is_superuser
@login_required
def send_invitation_email(request):
    """
        Sends a signup invitation link to the corresponding email address
    """
    user = request.user
    if request.method == "POST":
        user_form = SignupInvitationForm(request.POST)
        if user_form.is_valid():
            email = request.POST['email']
            invitation_type = request.POST['invitation_type']
            if invitation_type=="Courier":
                token_type = 1
            else:
                token_type = 2
            signup_link = user_handler.get_signup_invitation_url(email,token_type)
            logger.debug("invitation link is %s", signup_link)
            email_details = user_handler.prepSignupNotification(signup_link)
            logger.debug("What goes in the email is \n %s", email_details)
            email_notifier.send_signup_invitation(email, email_details)
            request.session['alert_message'] = dict(type="success",message="The signup link has been sent to your {0}".format(email))
            return redirect('home')

        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)

    user_form = SignupInvitationForm()
    return render(request, 'signupinvitation.html', locals())

@is_signup_token_alive
def signup_by_invitation(request):
    """Signup, if request == POST, creates the user"""
    ## if authenticated redirect to user's homepage directly ##
    logging.warn(request.POST)
    user = request.user
    if request.user.is_authenticated():
        return redirect('home')

    if request.GET['questr_token']:
        questr_token = request.GET['questr_token']
        try:
            prev_token = UserToken.objects.get(token=questr_token)
            logger.debug("prev_token")
            logger.debug(prev_token)
            if prev_token:
                logger.debug("transctional status")
                logger.debug(prev_token.status)
                if not prev_token.status:
                    if request.method == "POST":
                        user_form = QuestrUserCreationForm(request.POST)
                        if user_form.is_valid():
                            useraddress = dict(city=user_form.cleaned_data['city'], streetaddress=user_form.cleaned_data['streetaddress'],\
                                postalcode=user_form.cleaned_data['postalcode'])
                            logging.warn(useraddress)
                            userdata = user_form.save(commit=False)
                            userdata.address = json.dumps(useraddress)
                            userdata.phone = user_form.cleaned_data['phone']
                            if userdata.email != prev_token.email:
                                request.session['alert_message'] = dict(type="warning",message="The email provided was not the email the invitation was sent to!")
                                return redirect('index')
                            if prev_token.token_type==1:
                                userdata.is_shipper = True
                            else:
                                userdata.is_shipper = False
                            userdata.save()
                            authenticate(username=userdata.email, password=userdata.password)
                            userdata.backend='django.contrib.auth.backends.ModelBackend'
                            auth_login(request, userdata)
                            prev_token.status = True
                            prev_token.save()
                            verf_link = user_handler.get_verification_url(userdata)
                            logger.debug("verification link is %s", verf_link)
                            email_details = user_handler.prepWelcomeNotification(userdata, verf_link)
                            logger.debug("What goes in the email is \n %s", email_details)
                            email_notifier.send_email_notification(userdata, email_details)
                            pagetitle = "Please verify your email !"
                            return redirect('home')
                        if user_form.errors:
                            logger.debug("Login Form has errors, %s ", user_form.errors)
                        pagetitle = "Signup By invitation"
                        return render(request, 'signupbyinvitation.html', locals())
                    else:
                        user_form = QuestrUserCreationForm()
                        questr_token = request.GET['questr_token']
                        pagetitle = "Signup"
                        return render(request, 'signupbyinvitation.html', locals())
        except prev_token.DoesNotExist:
            return redirect('home')
    return redirect('home')


