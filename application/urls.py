from django.conf.urls import patterns, url
import views as applicationviews

urlpatterns = patterns(
    '',
    url(r'courier/$', applicationviews.applyAsCourier, name='applyAsCourier'),
    url(r'user/$', applicationviews.applyAsUser, name='applyAsUser'),
)
