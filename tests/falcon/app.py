
import falcon
from falcon_redis_cache.middleware import RedisCacheMiddleware
from tests.falcon.constants import REDIS_HOST, REDIS_PORT
from tests.falcon.resource import TestResource, TestUniqueResource, TestCollectionResource, DebugResource

api = falcon.API(middleware=[RedisCacheMiddleware(redis_host=REDIS_HOST, redis_port=REDIS_PORT)])

api.add_route(TestResource.route, TestResource())
api.add_route(TestUniqueResource.route, TestUniqueResource())
api.add_route(TestCollectionResource.route, TestCollectionResource())
api.add_route(DebugResource.route, DebugResource())
