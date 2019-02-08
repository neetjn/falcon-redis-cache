from falcon_redis_cache.hooks import CacheProvider
from falcon_redis_cache.resource import CacheCompaitableResource


class TestResource(CacheCompaitableResource):

    route = '/test/{test_id}/'

    def on_get(self, req, resp, test_id):
        pass

    def on_put(self, req, resp, test_id):
        pass

    def on_delete(self, req, resp, test_id):
        pass


class TestUniqueResource(CacheCompaitableResource):

    route = '/test/unique/{test_id}/'
    unique_cache = True

    def on_get(self, req, resp, test_id):
        pass

    def on_put(self, req, resp, test_id):
        pass

    def on_delete(self, req, resp, test_id):
        pass


class TestCollectionResource(CacheCompaitableResource):

    route = '/test/'
    cache_with_query = True

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        pass


TestResource.binded_resoures = [TestCollectionResource]
