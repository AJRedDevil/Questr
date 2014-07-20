from django.conf.urls import patterns, include, url
import views as mainview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', mainview.index, name="mainindex"),
    url(r'loadpage/(?P<template>[-_\w/.]+)$', mainview.loadPage, ),    
    url(r'^beta/', include('beta.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^quest/', include('quests.urls') ),
    url(r'^questrreview/', mainview.questrReview, name='questReview' ),
    url(r'^questreview/', mainview.questReview ),
    url(r'^review/', include('reviews.urls')),
    url(r'^contactus/', mainview.contactUs, name='contactus' ),
    url(r'^aboutus/', mainview.aboutUs, name='aboutus' ),
    url(r'^news/', mainview.news, name='news' ),
    url(r'^joinus/', mainview.joinus, name='joinus' ),
    url(r'^why/', mainview.whyQuestr, name='whyquestr' ),
    url(r'^trust/', mainview.trust, name='trust' ),
    url(r'^terms/', mainview.terms, name='terms' ),
    url(r'^faq/', mainview.faq, name='faq' ),
)