import redis
from string import Template
from .resource import CacheCompaitableResource
from .utils import cache_key


class HttpMethods(object):

    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


class RedisCacheMiddleware(object):

    def __init__(self, redis_host, redis_port, redis_db=0):
        self.client = redis.StrictRedis(redis_host, redis_port, redis_db)

    def process_resource(self, req, resp, resource, params):
        """Provide redis cache with every request."""
        if isinstance(resource, CacheCompaitableResource) and resource.use_cache:
            req.context.setdefault('params', params)
            resp.context.setdefault('cached', self.client.get(cache_key(req, resource)))

    def process_response(self, req, resp, resource, req_succeeded):
        """Sets or deletes cache for provided resources."""
        if req_succeeded and isinstance(resource, CacheCompaitableResource) and resource.use_cache:
            cache = cache_key(req, resource)
            if req.method == HttpMethods.GET:
                if not resp.body:
                    resp.body = resp.context.get('cached')
                self.client.set(cache, resp.body)
            else:
                self.client.delete(cache)
                params = req.context.get('params')
                for resc in resource.binded_resources:
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
                        for key in self.client.scan_iter('{}*'.format(_cache[:-1])):
                            self.client.delete(key)
