from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'questr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('en.urls')),
    url(r'^en/', include('en.urls')),
    url(r'^user/', include('en.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
