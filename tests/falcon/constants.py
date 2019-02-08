import os

REDIS_HOST = os.environ.get('REDIS_HOST', '0.0.0.0')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
