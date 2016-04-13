from django.shortcuts import render
from django.http import HttpResponse
import json

from codesearch import codesearch


def home_view(request):
    return render(
        request,
        'codeapp/home.html',
        {
            'title': 'Code search',
        }
    )


def rendered_search_view(request):
    q = request.GET['q']
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
    q = request.GET['q']
    res, out = codesearch.search_deep(q)
    response = HttpResponse(json.dumps(out), mimetype='application/json')
    return response


def more(request, what, nid):
    mid = {'def': 2, 'prev': 4, 'ctx': 6, 'next': 8, 'prod': 10}[what]
    out = {
        'code': [(mid, '%s de %s' % (what, nid))],
    }
    return HttpResponse(json.dumps(out), mimetype='application/json')


if __name__ == '__main__':
    results = search('some request')
    print(results)
