from django.conf.urls import patterns, include, url
from django.conf import settings

import views as apiview
import rest_framework_swagger

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
urlpatterns = patterns('',
    # Examples:
    url(r'^api-auth/$', views.obtain_auth_token),
    url(r'^quests/$', apiview.QuestsList.as_view()),
    url(r'^quests/(?P<pk>[0-9]+)/$', apiview.QuestsDetail.as_view()),
    url(r'^getprice/$', apiview.PriceCalculator.as_view()),
    url(r'^setstatus/$', apiview.AvailabilityStatus.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)

urlpatterns = format_suffix_patterns(urlpatterns)
