from django.conf.urls import patterns, include, url

import codeserve.urls

urlpatterns = patterns(
    '',
    url(r'^code/', include(codeserve.urls)),
)
