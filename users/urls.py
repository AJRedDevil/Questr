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
    url(r'^settings/password$', userviews.changePassword, name='changepassword'),
    url(r'^settings/card$', userviews.cardSettings, name='cardsettings'),
    url(r'^settings/email$', userviews.emailSettings, name='emailsettings'),
    url(r'^logout/$', userviews.logout, name='logout'),
    url(r'^verifymail$', userviews.resend_verification_email, name='verify_Email'),
    url(r'^email/confirm/(?P<user_code>[\w\d]+)', userviews.verify_email),
    url(r'^trades/$', userviews.myTrades, name='mytrades' ),
    url(r'^posts/$', userviews.myPosts, name='myposts' ),
    url(r'^forgotpassword/$', userviews.resetpassword, name='reset_password'),
    url(r'^(?P<displayname>[-_\w/.]+)/$', userviews.getUserInfo, name='getUserInfo'),

)