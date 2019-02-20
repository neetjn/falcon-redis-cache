import redis
from logging import warning
from string import Template


class HttpMethods(object):

    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


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


class RedisCacheMiddleware(object):

    def __init__(self, redis_host, redis_port, redis_db=0):
        self.client = redis.StrictRedis(redis_host, redis_port, redis_db)

    def process_resource(self, req, resp, resource, params):
        """Provide redis cache with every request."""
        if hasattr(resource, 'use_cache') and resource.use_cache:
            req.context.setdefault('params', params)
            resp.context.setdefault('cached', self.client.get(cache_key(req, resource)))

    def process_response(self, req, resp, resource, req_succeeded):
        """Sets or deletes cache for provided resources."""
        if req_succeeded and hasattr(resource, 'use_cache') and resource.use_cache:
            cache = cache_key(req, resource)
            if req.method == HttpMethods.GET:
                if not resp.body:
                    resp.body = resp.context.get('cached')
                self.client.set(cache, resp.body)
            else:
                self.client.delete(cache)
                params = req.context.get('params')
                for resc in resource.binded_resoures:
                    # interpolate for safe formatting
                    tmpl = resc.route.replace('{', '${')
                    # assumes that binded resources ay have routes with similar params
                    route = Template(tmpl).safe_substitute(**params)
                    # remove last character, uri has final slash stripped
                    uri = '{}://{}{}'.format(req.scheme, req.netloc, route)
                    # delete binded cached resources
                    _cache = cache_key(req, resc, uri)
                    self.client.delete(_cache)
                    if resc.cache_with_query:
                        # for resources using query strings
                        for key in self.client.scan_iter(_cache):
                            self.client.delete(key)
