from django.conf.urls import patterns, url

from beta import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^thankyou/', views.thankyou, name='thankyou'),
)
