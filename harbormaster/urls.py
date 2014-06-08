from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'harbormaster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'theharbor.views.index', name='index'),
    url(r'^data/$', 'theharbor.views.get_json_data', name='json'),
    url(r'^prep/$', 'theharbor.views.prep_docker', name='prep'),
    url(r'^ship/$', 'theharbor.views.start_docker', name='ship'),
    url(r'^ship/(?P<object_id>\w+)/$', 'theharbor.views.start_docker', name='ship'),    
    url(r'^pack/$', 'theharbor.views.pack_to_ship', name='pack'),

    # url(r'^tryz/$', 'theharbor.views.instance_name', name='tryz'),

)
