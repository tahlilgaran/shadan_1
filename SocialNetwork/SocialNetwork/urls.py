from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'users.views.login_site', name='login'),
    url(r'^login/$' , 'users.views.login_site' , name = 'login'),
     url(r'^logout/$' , 'users.views.logout_view'),
    url(r'^forgetpassword/$' , 'users.views.forget_pwd' , name = 'forget'),
    url(r'^signup/$' , 'users.views.signup' , name = 'signup'),
    url(r'^timeline/(?P<username>\w+)/$' , 'network.views.timeline'),
    url(r'^onepost/(?P<username>\w+)/(?P<post_id>\d+)/$' , 'network.views.onepost'),
     url(r'^addcomment/$', 'network.views.add_comment'),
     url(r'^like/$', 'network.views.like'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #userprifile
    url(r'^profile/(?P<username>\w+)/$' , 'network.views.user_profile'),
    url(r'^profile/(?P<username>\w+)/(?P<change>\w+)/$' , 'network.views.user_profile'),
    url(r'^film/(?P<film_id>\d+)/$', 'network.views.film_profile'),
    url(r'^follow/(?P<follow>\w+)/(?P<username>\w+)/$' , 'network.views.follow'),
    url(r'^search/(?P<kind>\w+)/$' , 'network.views.search'),
    url(r'^search/(?P<kind>\w+)/(?P<value>\w+)/$' , 'network.views.search'),

)
