from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'questr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('beta.urls')),
    url(r'^en/', include('en.urls', namespace="en")),
    url(r'^user/', include('en.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^beta/', include('beta.urls', namespace="beta")),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)
