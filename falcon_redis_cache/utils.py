import inject
import redis
from logging import warning
from string import Template
from .resource import CacheCompaitableResource


def cache_key(req, resource, uri=None):
    """Provides unique redis cache key."""
    uri = uri or req.uri
    if uri.endswith('/'):
        uri = uri[:-1]
    if resource.unique_cache:
        if req.auth:
            return '{}+{}'.format(uri, req.auth)
        warning(req, 'Could not construct unique key for uri "{}"'.format(uri))
    return uri


@inject.params(redis_client=redis.Redis)
def clear_resource_cache(resource, req, redis_client=None, **params):
    if issubclass(resource, CacheCompaitableResource) and redis_client:
        tmpl = resource.route.replace('{', '${')
        route = Template(tmpl).safe_substitute(**params)
        uri = '{}://{}{}'.format(req.scheme, req.netloc, route)
        _cache = cache_key(req, resource, uri)
        redis_client.delete(_cache)
        if resource.cache_with_query:
            # for resources using query strings
            for key in redis_client.scan_iter('{}*'.format(_cache[:-1])):
                redis_client.delete(key)
