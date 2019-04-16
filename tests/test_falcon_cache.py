import datetime
import time
from falcon import testing
from tests.falcon.app import api
from tests.falcon.resource import MAX_SLEEP_TIME


class HrefMap(object):
    TEST = '/test/{test_id}/'
    TEST_BINDED = '/test/binded/{test_id}/action/'
    TEST_UNIQUE = '/test/unique/{test_id}/'
    COLLECTION = '/test/'
    DEBUG = '/test/debug/'


MAX_RESPONSE_TIME = 2.5


class FalconCacheTest(testing.TestCase):

    def setUp(self):
        super(FalconCacheTest, self).setUp()
        self.app = api

        # monkey patch GET to include elapsed response time
        get_method = self.simulate_get
        def wrapper(href, headers=None, params=None):
            initial_time = time.time()
            response = get_method(href, headers=headers, params=params)
            response.elapsed_time = time.time() - initial_time
            return response
        self.simulate_get = wrapper

        # wipe database
        wipe_res = self.simulate_delete(HrefMap.DEBUG)
        self.assertEqual(wipe_res.status_code, 204)

    def assertUncachedResponse(self, res):
        self.assertGreaterEqual(res.elapsed_time, MAX_RESPONSE_TIME)
        self.assertGreaterEqual(MAX_SLEEP_TIME + MAX_RESPONSE_TIME, res.elapsed_time)

    def assertCachedResponse(self, res):
        self.assertLessEqual(res.elapsed_time, MAX_SLEEP_TIME)

    def test_base_cache(self):
        # response should not be cached
        res = self.simulate_get(HrefMap.COLLECTION)
        self.assertEqual(res.status_code, 200)
        self.assertUncachedResponse(res)
        # response should now be cached
        cached_res = self.simulate_get(HrefMap.COLLECTION)
        self.assertEqual(cached_res.status_code, 200)
        self.assertCachedResponse(cached_res)

    def test_binded(self):
        res = self.simulate_get(HrefMap.COLLECTION)
        self.assertEqual(res.status_code, 200)
        test_id = res.json[-1].get('_id')
        resource_res = self.simulate_get(HrefMap.TEST.format(test_id=test_id))
        self.assertEqual(resource_res.status_code, 200)
        self.assertUncachedResponse(resource_res)
        cached_resource_res = self.simulate_get(HrefMap.TEST.format(test_id=test_id))
        self.assertCachedResponse(cached_resource_res)
        binded_res = self.simulate_post(HrefMap.TEST_BINDED.format(test_id=test_id))
        self.assertEqual(binded_res.status_code, 200)
        cleared_cache_res = self.simulate_get(HrefMap.TEST.format(test_id=test_id))
        self.assertUncachedResponse(cleared_cache_res)

    def test_unique_cache(self):
        res = self.simulate_get(HrefMap.COLLECTION)
        self.assertEqual(res.status_code, 200)
        test_id = res.json[-1].get('_id')
        headers = {'Authorization': 'somerandomkey'}
        # response for unique resource should not be cached
        resource_res = self.simulate_get(HrefMap.TEST_UNIQUE.format(test_id=test_id), headers=headers)
        self.assertEqual(resource_res.status_code, 200)
        self.assertUncachedResponse(resource_res)
        # response with unique resource is not cached
        cached_resource_res = self.simulate_get(HrefMap.TEST_UNIQUE.format(test_id=test_id), headers=headers)
        self.assertCachedResponse(cached_resource_res)
        # response should not be cached using new auth header
        resource_res_unauthorized = self.simulate_get(HrefMap.TEST_UNIQUE.format(test_id=test_id), headers={
            'Authorization': 'somenewkey'})
        self.assertUncachedResponse(resource_res_unauthorized)

    def test_cache_with_query(self):
        params = {'start': 5, 'count': 5}
        # response should not be cached
        res = self.simulate_get(HrefMap.COLLECTION, params=params)
        self.assertEqual(res.status_code, 200)
        self.assertUncachedResponse(res)
        # response should now be cached
        cached_res = self.simulate_get(HrefMap.COLLECTION, params=params)
        self.assertEqual(cached_res.status_code, 200)
        self.assertCachedResponse(cached_res)
        # response with different params should not be cached
        res = self.simulate_get(HrefMap.COLLECTION, params={'start': 10, 'count': 5})
        self.assertEqual(res.status_code, 200)
        self.assertUncachedResponse(res)
        # invalid should wipe all cache
        test_id = res.json[-1].get('_id')
        delete_res = self.simulate_delete(HrefMap.TEST.format(test_id=test_id))
        self.assertEqual(delete_res.status_code, 204)
        res = self.simulate_get(HrefMap.COLLECTION, params=params)
        # assumes cache binding works, invalidates requests with query strings as well
        self.assertUncachedResponse(res)
