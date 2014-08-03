import json
from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.template.loader import render_to_string
import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.core import serializers
import datetime
import json
import decimal
from sets import Set
import collections
from django.core.cache import cache
import settings
from django.db import models
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder

def json_view( view_func ):
    @wraps( view_func, assigned = available_attrs( view_func ) )
    def _wrapped_view( request, *args, **kwargs ):
        response = view_func( request, *args, **kwargs )
        if isinstance(response, HttpResponse):
            return response
        return HttpResponse(to_json(response), mimetype='application/json')
    return _wrapped_view


def cacheable( view_func ):
    @wraps( view_func, assigned = available_attrs( view_func ) )
    def _wrapped_view( request, *args, **kwargs ):
        if request.method == 'GET':
            key = settings.CACHE_STRING % (request.get_full_path(), 'ajax', request.is_ajax())
            cached = cache.get(key)
            if cached:
               print 'HIT CACHE'
               return cached
            response = view_func( request, *args, **kwargs )
            cache.set(key, response, settings.CACHE_TIME)
            return response
        else:
            return view_func( request, *args, **kwargs )
    return _wrapped_view


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime.datetime):
            return str(o)
        elif isinstance(o, models.Model):
            return o.deep()
        elif isinstance(o, collections.Iterable):
            if len(o) > 0 and hasattr(o[0], 'shallow'):
                return [p.shallow() for p in o]
            return list(o)
        return super(CustomEncoder, self).default(o)



def to_json(data):
    return json.dumps(data, cls=CustomEncoder)