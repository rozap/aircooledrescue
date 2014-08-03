from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('core.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^register$', 'register', name='register'),
    url(r'^about$', 'about', name='about'),
    url(r'^retrieve$', 'retrieve', name='retrieve'),
    url(r'^reset_password/(?P<key>[\w\-]+)$', 'reset_password', name='reset_password'),
    url(r'^activate/(?P<key>[\w\-]+)$', 'activate', name='activate'),

    # url(r'^buspeople/', include('buspeople.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
