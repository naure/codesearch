from django.conf.urls import patterns, url

from codeserve import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home_view),
    url(r'^search$', views.search),
    url(r'^more/(?P<what>\w+)/(?P<nid>\d+)$', views.more),
)
