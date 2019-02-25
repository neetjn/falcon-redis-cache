import json
import redis
import time
import os
import falcon
from falcon.errors import HTTPBadRequest, HTTPNotFound
from falcon_redis_cache.hooks import CacheProvider
from falcon_redis_cache.resource import CacheCompaitableResource

from tests.falcon.constants import REDIS_HOST, REDIS_PORT


MAX_SLEEP_TIME = int(os.environ.setdefault('MAX_SLEEP_TIME', '5'))
Resources = [{'_id': str(n), 'name': '{}-budget'.format(n)} for n in range(5)]


def get_resource(_id: str) -> dict:
    """Get existing resource by id"""
    return next(r for r in Resources if r.get('_id') == _id)


def update_resource(_id: str, change: dict):
    """Update existing resource by id"""
    resource = get_resource(_id)
    resource.update(change)


def delete_resource(_id: str):
    """Delete existing resource by id"""
    resource = get_resource(_id)
    global Resources
    Resources = [r for r in Resources if r.get('_id') != resource.get('_id')]


def create_resource(resource):
    """Create a new resource"""
    resource.update({'_id': str(int(time.time()))})
    Resources.append()


class DebugResource(CacheCompaitableResource):

    route = '/test/debug/'

    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_204
        client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        client.flushall()
        client.flushdb()


class TestResource(CacheCompaitableResource):

    route = '/test/{test_id}/'

    @CacheProvider.from_cache
    def on_get(self, req, resp, test_id):
        time.sleep(MAX_SLEEP_TIME)
        try:
            resource = get_resource(test_id)
        except StopIteration:
            raise HTTPNotFound()
        resp.body = json.dumps(resource)

    def on_put(self, req, resp, test_id):
        resp.status = falcon.HTTP_204
        payload = json.loads(req.stream.read())
        if '_id' not in payload or not isinstance(payload.get('_id'), str):
            raise HTTPBadRequest()
        try:
            update_resource(test_id, payload)
        except StopIteration:
            raise HTTPNotFound()

    def on_delete(self, req, resp, test_id):
        resp.status = falcon.HTTP_204
        try:
            delete_resource(test_id)
        except StopIteration:
            raise HTTPNotFound()


class TestUniqueResource(TestResource):

    route = '/test/unique/{test_id}/'
    unique_cache = True


class TestCollectionResource(CacheCompaitableResource):

    route = '/test/'
    cache_with_query = True

    @CacheProvider.from_cache
    def on_get(self, req, resp):
        time.sleep(MAX_SLEEP_TIME)
        resp.body = json.dumps(Resources)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        payload = json.loads(req.stream.read())
        create_resource(payload)


TestResource.binded_resources = [TestCollectionResource]
