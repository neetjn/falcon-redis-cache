from falcon_redis_cache.hooks import CacheProvider
from falcon_redis_cache.resource import CacheCompaitableResource


class TestResource(CacheCompaitableResource):

    route = '/test/{test_id}/'


    def on_get(self, req, resp, test_id):
        pass


class TestUniqueResource(CacheCompaitableResource):

    route = '/test/unique/{test_id}/'


    def on_get(self, req, resp, test_id):
        pass


class TestCollectionResource(CacheCompaitableResource):

    route = '/test/'


    def on_get(self, req, resp):
        pass
