from django.conf.urls import patterns, url

import views as userviews

urlpatterns = patterns('',
    url(r'^$', userviews.signin, name='user'),
    # url(r'^signup/$', userviews.signup, name='signup'),
    url(r'^signin/$', userviews.signin, name='signin'),
    url(r'^home/$', userviews.home, name='home'),
    # url(r'^profile/$', userviews.profile, name='profile'),
    # url(r'^profile/save/.*', userviews.saveUserInfo, name='saveprofile'), # commented for later use
    url(r'^createcourier/$', userviews.createcourier, name='createcourier'),
    url(r'^createuser/$', userviews.createuser, name='createuser'),
    url(r'^settings/$', userviews.userSettings, name='settings'),
    url(r'^settings/password$', userviews.changePassword, name='changepassword'),
    # url(r'^settings/notification$', userviews.notificationsettings, name='notificationsettings'),
    url(r'^logout/$', userviews.logout, name='logout'),
    url(r'^verifymail$', userviews.resend_verification_email, name='verify_Email'),
    url(r'^email/confirm/', userviews.verify_email),
    url(r'^forgotpassword/$', userviews.resetpassword, name='reset_password'),
    url(r'^passwordreset/$', userviews.createpassword, name='createpassword'),
    url(r'^changestatus/$', userviews.changestatus, name='changestatus'),
    url(r'^invite/$', userviews.send_invitation_email, name='send_invitation_email'),
    # url(r'^(?P<displayname>[-_\w/.]+)/$', userviews.getUserInfo, name='getUserInfo'),
)
