from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('api.views',
    # Examples:
    url(r'^people$', 'people', name='people'),
    url(r'^people/(?P<id>\d+)$', 'person', name='person'),
    url(r'^people/(?P<id>\d+)/karma$', 'karma', name='karma'),
    url(r'^people/(?P<id>\d+)/flags$', 'flags', name='flags'),
    url(r'^profile/(?P<id>\d+)$', 'profile', name='profile'),
    url(r'^services$', 'services', name='services'),

    # url(r'^buspeople/', include('buspeople.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
