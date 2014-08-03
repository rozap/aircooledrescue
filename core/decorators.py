import json
from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.template.loader import render_to_string
import settings
from django.core.cache import cache

def json_view( view_func ):
    @wraps( view_func, assigned = available_attrs( view_func ) )
    def _wrapped_view( request, *args, **kwargs ):
        response = view_func( request, *args, **kwargs )
        status_code = 200
        if isinstance( response, HttpResponse ):
            return response
        elif isinstance( response, tuple ):
            response, status_code = response

        if not isinstance( response, str ):
            response = json.dumps( response )
        return HttpResponse( response, mimetype = 'application/json', status = status_code )
    return _wrapped_view


def cacheable( view_func ):
    @wraps( view_func, assigned = available_attrs( view_func ) )
    def _wrapped_view( request, *args, **kwargs ):
        if request.method == 'GET':
            #key = settings.CACHE_PREFIX % (request.get_full_path(), 'ajax', request.is_ajax())
           # cached = cache.get(key)
            #if cached:
            #    print 'HIT CACHE'
            #    return cached
            response = view_func( request, *args, **kwargs )
            #cache.set(key, response, settings.CACHE_TIME)
            return response
        else:
            return view_func( request, *args, **kwargs )
    return _wrapped_view