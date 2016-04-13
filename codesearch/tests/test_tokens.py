import os
from unittest import TestCase
from codesearch.tokens import tokenize, learn, sample
from pprint import pprint
from time import time


code = '''
def proxy_view(request, path, remoteurl, upstream_headers={}):
    #
        # Download the response from upstream
    response = raw_proxy_view(
        request,
        some_global,
        url='/'.join((remoteurl, path)),
        requests_args={
            'headers': upstream_headers,
            'allow_redirects': False,
        },
    ) or 'Oups'

    # Handle absolute redirections
    location = response.get('LOCATION')
    if location:
        match = re_abs_url.match(location)
        if match:
            print('Absolute redirect to ' + location)
            domain, query = match.groups()
            # XXX `query` must not contain the upstream prefix
            # XXX `path` has the query string in there
            prefix = request.path_info[:-len(path) or None]  # Url to this view
            new_path = query and query[1:] or ''  # Next view `path` parameter
            response['LOCATION'] = prefix + new_path
            print('Rewritten as %s + %s' % (prefix, new_path))

    return response
'''

class TestToken(TestCase):
    def test_tokens(self):
        tokens = tokenize(code)
        expect = [
            '\n',
            'def', ' ', 'proxy_view', '(',
            'request', ',', ' ',
            'path', ',', ' ',
            'remoteurl', ',', ' ',
            'upstream_headers', '=', '{', '}', ')', ':', '\n',
            '    ', '#', '\n',
            '    ', '    ', '#',
        ]
        self.assertEqual(tokens[:len(expect)], expect)

    def test_learn(self):
        # 20 états, 20 fichiers, 20 itérations = 10 minutes

        obs = []
        for root, dirnames, filenames in os.walk('..'):
            for filename in filenames:
                if len(obs) >= 20:
                    break
                if filename.endswith('.py'):
                    path = os.path.join(root, filename)
                    try:
                        with open(path) as fd:
                            source = fd.read()
                            if source:
                                print(path)
                                obs.append(tokenize(source))
                    except Exception as e:
                        print(e)
        start = time()
        model, i2t, t2i = learn(obs, n_states=20)
        stop = time()
        import IPython; IPython.embed()


