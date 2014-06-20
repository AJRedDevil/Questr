from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from social.backends.google import GooglePlusAuth ###disabled google plus##

def index(request):
    if request.user.is_authenticated():
        return redirect('home')
    nav_link_1 = "/user/login"
    nav_link_1_label = "login"
    nav_link_2 = "/user/signup"
    nav_link_2_label ="signup"
    nav_link_3 = "#"
    nav_link_3_label ="about us"
    # plus_id = getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None) ###disabled google plus##
    # plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE) ###disabled google plus##
    return render(request, 'index.html', locals())

def loadPage(request, template):
    return render(request, template, locals())

def questReview(request):
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    return render(request, 'questReview.html', locals())

def questrReview(request):
    pagetype="loggedin"
    user = request.user
    nav_link_1 = "/user/profile"
    nav_link_1_label = "my profile"
    nav_link_2 = "/user/settings"
    nav_link_2_label ="settings"
    nav_link_3 = "/user/logout"
    nav_link_3_label ="logout"
    return render(request, 'questrReview.html', locals())