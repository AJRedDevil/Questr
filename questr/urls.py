from django.conf.urls import patterns, include, url
import views as mainview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', mainview.index, name="index"),
    url(r'loadpage/(?P<template>[-_\w/.]+)$', mainview.loadPage, ),    
    url(r'^beta/', include('beta.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^quest/', include('quests.urls') ),
    url(r'^trades/', mainview.myTrades ),
)