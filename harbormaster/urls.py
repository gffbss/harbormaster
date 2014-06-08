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
    url(r'^start/$', 'theharbor.views.start_docker', name='start'),
    url(r'^prep/$', 'theharbor.views.pack_to_ship', name='pack'),
)
