from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static 
from users.views import login
import views as mainview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', mainview.index, name="index"),
    url(r'loadpage/(?P<template>[-_\w/.]+)$', mainview.loadPage, ),    
    url(r'^beta/', include('beta.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^quests/', mainview.quests ),
    url(r'^quest/', mainview.quest ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)