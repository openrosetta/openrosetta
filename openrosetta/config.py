import datetime
import simplejson as json
from cornice import Service

default_cors_policy = {'origins': ('*', )}


class RService(Service):
    def __init__(self, name, path, description=None, cors_policy=default_cors_policy, renderer='jsonwithdate', **kw):
        # To work properly with venusian, we have to specify the number of
        # frames between the call to venusian.attach and the definition of
        # the attached function. Cornice defaults to 1, and we add another.
        depth = 2
        super(RService, self).__init__(name, path, description=description, cors_policy=cors_policy,
                                       depth=depth, renderer=renderer, **kw)


def json_renderer(helper):
    return _JsonRenderer()


class _JsonRenderer(object):
    def __call__(self, data, context):
        acceptable = ('application/json', 'text/json', 'text/plain')
        response = context['request'].response
        content_type = (context['request'].accept.best_match(acceptable)
                        or acceptable[0])
        response.content_type = content_type
        if hasattr(data, '__json__'):
            data = data.__json__()
        return json.dumps(_json_convert(data), use_decimal=True)


def _json_convert(obj):
    if hasattr(obj, 'iteritems') or hasattr(obj, 'items'):  # PY3 support
        return dict(((k, _json_convert(v)) for k, v in obj.iteritems()))
    elif hasattr(obj, '__iter__') and not isinstance(obj, basestring):
        return list((_json_convert(v) for v in obj))
    try:
        return default(obj)
    except TypeError:
        return obj


def default(obj):
    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        return obj.isoformat()
    raise TypeError("%r is not JSON serializable" % obj)


def includeme(config):
    config.add_renderer('jsonwithdate', json_renderer)
