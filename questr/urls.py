from django.conf.urls import patterns, include, url
import views as mainview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', mainview.index, name="index"),
    url(r'^join$', mainview.join, name='join'),
    url(r'^contactus$', mainview.contactus, name='contactus'),

    url(r'loadpage/(?P<template>[-_\w/.]+)$', mainview.loadPage, ),    
    url(r'^user/', include('users.urls')),
    url(r'^quest/', include('quests.urls') ),
    url(r'^questrreview/', mainview.questrReview, name='questReview' ),
    url(r'^questreview/', mainview.questReview ),
    url(r'^review/', include('reviews.urls')),

    url(r'^contact/', mainview.contact, name='contact' ),
    url(r'^news/', mainview.news, name='news' ),

    url(r'^company/join/', mainview.join, name='join' ),
    url(r'^company/about/', mainview.about, name='about' ),

    url(r'^terms/', mainview.terms, name='terms' ),
    url(r'^privacy/', mainview.privacy, name='privacy' ),    
    url(r'^help/faq/', mainview.faq, name='faq' ),
    url(r'^help/crowdshipping/', mainview.crowdshipping, name='crowdshipping' ),
    url(r'^help/trust/', mainview.trust, name='trust' ),
)