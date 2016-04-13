from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib.auth.decorators import login_required
from loginfront.views import login_view, logout_view, forward_view


def forward_to(upstream_servers, require_auth=True, **kwargs):
    " Forward all requests to upstream servers, after authentication. "
    if not upstream_servers:
        raise ValueError('No upstream servers configured')
    return include(patterns('', url(
        r'^(?P<path>.*)',
        login_required(forward_view) if require_auth else forward_view,
        {
            'remoteurls': upstream_servers,
        },
        **kwargs
    )))


# Access the loginfront views (login, logout)
urlpatterns = patterns(
    '',
    url(r'^$',
        login_view,
        {
            'template_name': 'loginfront/home.html',
            'extra_context': {
                'title': settings.SITE_TITLE,
                'forward_urls': settings.FORWARD_URLS,
            },
        },
        name='loginfront'),
    url(r'^logout$',
        logout_view,
        {'login_url': settings.LOGIN_URL + '?next=.'},
        name='loginfront_logout'),
)
