# falcon-redis-cache

[![build](https://travis-ci.org/neetjn/falcon-redis-cache.svg?branch=master)](https://travis-ci.org/neetjn/falcon-redis-cache)
[![PyPI version](https://badge.fury.io/py/falcon-redis-cache.svg)](https://badge.fury.io/py/falcon-redis-cache)

Redis cache middleware for falcon resources. Pulled from py-blog project @ https://github.com/neetjn/py-blog

## About

**falcon-redis-cache** is a very simple middlware for the Falcon Web/REST framework for Python. This middleware caches resources over the wire using Redis, and helps both simplify and automate redundant tasks such as serving responses directly from cache.

## Use

This project should be compaitable with any version of Falcon. Support is available for both Python 2.7 and 3.4+.

**falcon-redis-cache** can be installed with pip like so:

```bash
pip install falcon-redis-cache
```

Once installed, the middleware can be instantiated extending the Falcon api:

```python
import falcon
from falcon_redis_cache.middleware import RedisCacheMiddleware


api = falcon.API(middleware=[
  RedisCacheMiddleware(redis_host=..., redis_port=..., redis_db=...)
])
```

To ensure your resources are compatible, inherit from the provided resource:

```python
from falcon_redis_cache.resource import CacheCompaitableResource


class MyResource(CacheCompaitableResource):

  route = '/'

  # enabled by default
  # - tells middleware to enable caching on resource
  use_cache = True
  # disabled by default
  # - tells middleware to cache using auth credentials
  unique_cache = False
  # disabled by default
  # - tells middleware to process matching resources with unique query strings
  cache_with_query = False
  # list of resource definitions to clear cache from in the event of a change
  # for ex; if a post, put, or delete request is made on this resource...
  # any binded resources will have their caches cleaned
  binded_resources = []

  def on_get(self, req, res):
    ...

```

You may serve directly from cache without having Falcon hit responders by using the `from_cahe` hook:

```python
from falcon_redis_cache.hooks import CacheProvider


class ItemResource(CacheCompaitableResource):

  route = '/item/{item_id}/'

  @CacheProvider.from_cache
  def on_get(self, req, resp, item_id):
    # if resource already exists in cache, responder will not be processed by Falcon
    ...
```

## Contributors

* **John Nolette** (john@neetgroup.net)

Contributing guidelines are as follows,

* Any new features added must also be unit tested in the `tests` subdirectory.
  * Branches for bugs and features should be structured like so, `issue-x-username`.
* Include your name and email in the contributors list.

---

Copyright (c) 2019 John Nolette Licensed under the MIT license.

