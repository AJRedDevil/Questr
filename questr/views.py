from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from social.backends.google import GooglePlusAuth ###disabled google plus##

def index(request):
    if request.user.is_authenticated():
        return redirect('home')
    # plus_id = getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None) ###disabled google plus##
    # plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE) ###disabled google plus##
    return render(request, 'beta/index.html', locals())

def loadPage(request, template):
    return render(request, template, locals())

def questReview(request):
    pagetype="loggedin"
    user = request.user
    return render(request, 'questReview.html', locals())

def questrReview(request):
    pagetype="loggedin"
    user = request.user
    return render(request, 'questrReview.html', locals())