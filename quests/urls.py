from django.conf.urls import patterns, include, url

import views as questviews

urlpatterns = patterns('',
    url(r'^$', questviews.listallquests, name='listallquests'),
    url(r'^new/$', questviews.createquest, name='createquest'),
    url(r'^(?P<questname>[-_\w/.]+)/apply$', questviews.applyForQuest, name='applyforquest'),
    url(r'^(?P<questname>[-_\w/.]+)/edit$', questviews.editquest, name='editquest'),
    url(r'^(?P<questname>[-_\w/.]+)/$', questviews.viewquest, name='viewquest'),
)