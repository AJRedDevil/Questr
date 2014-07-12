from django.conf.urls import patterns, include, url

import views as questviews

urlpatterns = patterns('',
    url(r'^$', questviews.listallquests, name='listallquests'),
    url(r'^new/$', questviews.newquest, name='newquest'),
    url(r'^confirm/$', questviews.confirmquest, name='confirmquest'),
    url(r'^(?P<questname>[-_\w/.]+)/apply$', questviews.applyForQuest, name='applyforquest'),
    url(r'^(?P<questname>[-_\w/.]+)/withdraw$', questviews.withdrawFromQuest, name='withdrawfromquest'),
    url(r'^(?P<questname>[-_\w/.]+)/edit$', questviews.editquest, name='editquest'),
    url(r'^(?P<questname>[-_\w/.]+)/$', questviews.viewquest, name='viewquest'),
    url(r'(?P<questname>[-_\w/.]+)/delete$', questviews.deletequest, name='deletequest'),
    url(r'(?P<questname>[-_\w/.]+)/complete$', questviews.completequest, name='completequest'),
)