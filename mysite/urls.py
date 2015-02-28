from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import polls,hotgirl
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'fetchQzone.views.index', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

     #Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^polls/',include('polls.urls',namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^girl/',include('hotgirl.urls',namespace="girl")),
    url(r'^fetchQzone/',include('fetchQzone.urls',namespace='fetchQzone'))
)
