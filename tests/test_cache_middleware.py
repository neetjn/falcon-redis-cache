import datetime
import time
from falcon import testing
from tests.falcon.app import api
from tests.falcon.resource import MAX_SLEEP_TIME


class HrefMap:
    TEST = '/test/{test_id}/'
    TEST_UNIQUE = '/test/unique/{test_id}/'
    COLLECTION = '/test/'


class FalconCacheTest(testing.TestCase):

    def setUp(self):
        super(FalconCacheTest, self).setUp()
        self.app = api

        # monkey patch GET to include elapsed response time
        get_method = self.simulate_get
        def wrapper(href):
            initial_time = time.clock() * 1000
            response = get_method(href)
            response.elapsed_time = (time.clock() * 1000) - initial_time
            return response
        self.simulate_get = wrapper


    def test_foobar(self):
        # response should not be cached
        res = self.simulate_get(HrefMap.COLLECTION)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(MAX_SLEEP_TIME + 1, res.elapsed_time)
        # response should now be cached
        res = self.simulate_get(HrefMap.COLLECTION)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(MAX_SLEEP_TIME + 1, res.elapsed_time)
