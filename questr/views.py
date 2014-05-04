from django.shortcuts import render
# from django.conf import settings
# from social.backends.google import GooglePlusAuth ###disabled google plus##

def index(request):
    nextlink = "login"
    # plus_id = getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None) ###disabled google plus##
    # plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE) ###disabled google plus##
    return render(request, 'index.html', locals())

def loadPage(request, template):
    return render(request, template, locals())   