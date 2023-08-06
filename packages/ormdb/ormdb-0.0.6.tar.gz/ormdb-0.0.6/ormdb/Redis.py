#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
import redis as redis_client
from redis import StrictRedis, ConnectionPool



class Redis:
    @staticmethod
    def get_instance(host="localhost", port=6379, db=0, password=None):
        pool = ConnectionPool(host=host, port=port, db=db, password=password)
        redis = StrictRedis(connection_pool=pool)
        return redis

    @staticmethod
    def test_redis():
        redis=Redis.get_instance()
        redis.set('name','Frank')
        redis.sadd('a', 1, 2, 3)
        print redis.dbsize()
        print redis.get('name')
        print redis.smembers("a")



    @staticmethod
    def get_pipe(host="localhost", port=6379, db=0, password=None):
        r = redis_client.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
        pipe = r.pipeline()
        return pipe


Redis.test_redis()
