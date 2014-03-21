from django.conf.urls import patterns, url

from en import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>\d+)/$', views.user, name='user'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/done/$', views.signup_done, name='signup_done'),
)
