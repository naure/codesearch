from django.shortcuts import render
from django.http import HttpResponse
import json
import re

from codesearch import codesearch
from codesearch.codesearch import render_node_path
from codesearch import codeexplore


RE_NONALPHA = re.compile(r'[^\w-]')

def normalize(query):
    return RE_NONALPHA.sub('', query)


def home_view(request):
    return render(
        request,
        'codeapp/home.html',
        {
            'title': 'Code search',
        }
    )


def rendered_search_view(request):
    q = normalize(request.GET['q'])
    res, out = codesearch.search_deep(q)
    return render(
        request,
        'codeapp/results.html',
        {
            'title': 'Code search',
            'results': out,
        }
    )


def search(request):
    q = normalize(request.GET['q'])
    res, out = codesearch.search_deep(q)
    return HttpResponse(json.dumps(out), mimetype='application/json')


fake_handler = lambda what: (
    lambda nid: [{
        'id': nid + 1,
        'code': [(nid + hash(what)) % 20],
    }])


more_handlers = {
    'def': codeexplore.find_def_by_id,
    'pro': codeexplore.find_prod_by_id,
    'prev': fake_handler('prev'),
    'ctx': fake_handler('ctx'),
    'next': fake_handler('next'),
}

def more(request, what, nid):
    res = more_handlers[what](int(nid))
    out = [render_node_path(name, n, path) for name, n, path in res]
    return HttpResponse(json.dumps(out), mimetype='application/json')
