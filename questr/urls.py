from django.conf.urls import patterns, include, url
# from django.conf import settings

import views as mainview
import quests.views as questviews

urlpatterns = patterns('',
    # Examples:
    url(r'^$', mainview.index, name="index"),
    url(r'^contactus$', mainview.contactus, name='contactus'),

    url(r'loadpage/(?P<template>[-_\w/.]+)$', mainview.loadPage, ),    
    url(r'^user/', include('users.urls')),
    url(r'^quest/', include('quests.urls') ),
    url(r'^track/', questviews.tracking_number_search, name='trackquest'),

    # url(r'^questrreview/', mainview.questrReview, name='questReview' ),
    # url(r'^questreview/', mainview.questReview ),
    # url(r'^review/', include('reviews.urls')),

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

# if settings.DEBUG:
#     # static files (images, css, javascript, etc.)
#     urlpatterns += patterns('',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#         'document_root': settings.MEDIA_ROOT}))