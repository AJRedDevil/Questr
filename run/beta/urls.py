from django.conf.urls import patterns, url

from beta import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^join_beta/', views.join_beta, name='join_beta'),
    url(r'^thankyou/', views.thankyou, name='thankyou'),
)
