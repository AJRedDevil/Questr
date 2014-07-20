from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from social.backends.google import GooglePlusAuth ###disabled google plus##

def index(request):
    if request.user.is_authenticated():
        return redirect('home')
    # plus_id = getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None) ###disabled google plus##
    # plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE) ###disabled google plus##
    return render(request, 'index.html', locals())

def loadPage(request, template):
    return render(request, template, locals())

def contact(request):
    return render(request, 'contact.html', locals())

def about(request):
    return render(request, 'about.html', locals())

def news(request):
    return render(request, 'news.html', locals())

def join(request):
    return render(request, 'join.html', locals())

def crowdshipping(request):
    return render(request, 'crowdshipping.html', locals())

def trust(request):
    return render(request, 'trust.html', locals())

def terms(request):
    return render(request, 'terms.html', locals())

def privacy(request):
    return render(request, 'privacy.html', locals())

def faq(request):
    return render(request, 'faq.html', locals())

def questReview(request):
    pagetype="loggedin"
    user = request.user
    return render(request, 'questReview.html', locals())

def questrReview(request):
    pagetype="loggedin"
    user = request.user
    return render(request, 'questrReview.html', locals())