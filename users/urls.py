from django.conf.urls import patterns, include, url

import views as userviews

urlpatterns = patterns('',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', userviews.login, name='user'),
    url(r'^signup/$', userviews.signup, name='signup'),
    url(r'^login/$', userviews.login, name='login'),
    url(r'^home/$', userviews.home, name='home'),
    url(r'^profile/$', userviews.profile, name='profile'),
    url(r'^profile/save/.*', userviews.saveUserInfo, name='saveprofile'), # commented for later use
    url(r'^createpassword/$', userviews.createPassword, name='createpassword'),
    url(r'^settings/$', userviews.userSettings, name='settings'),
    url(r'^logout/$', userviews.logout, name='logout'),
    url(r'^(?P<displayname>[-_\w/.]+)/$', userviews.getUserInfo, name='getUserInfo'),
    url(r'^verifymail$', userviews.resend_verification_email, name='verify_Email'),
    url(r'^email/confirm/(?P<user_code>[\w\d]+)', userviews.verify_email),
)