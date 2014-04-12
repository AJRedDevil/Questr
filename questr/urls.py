from django.conf.urls import patterns, include, url

# from views import * as mainview
from users.views import login
import views as mainview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('beta.urls')),
    url(r'^beta/', include('beta.urls')),
    url(r'^user/', include('users.urls')),
)

