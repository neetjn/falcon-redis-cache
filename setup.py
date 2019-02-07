
# pylint: disable=missing-docstring
from setuptools import setup


setup(
    name='falcon-redis-cache',
    description='Redis cache middleware for falcon resources.',
    version='0.0.1',
    url='https://neetjn.github.io/falcon-redis-cache/',
    author='John Nolette',
    author_email='john@neetgroup.net',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=[
        'redis'
    ],
    packages=['falcon_redis_cache']
)
