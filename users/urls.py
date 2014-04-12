from django.conf.urls import patterns, include, url

import views as userviews

urlpatterns = patterns('',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', userviews.login, name='home'),
    url(r'^login/$', userviews.login, name='login'),
    url(r'^profile/$', userviews.profile, name='profile'),
    url(r'^logout/$', userviews.logout, name='logout'),
)