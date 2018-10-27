# -*- coding: utf-8 -8-

import redis


class RedisUtil:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = redis.StrictRedis(host=self.host, port=self.port)

    def check(self):
        print(self.conn.info())

    def set(self, key, value):
        self.conn.set(key, value)

    def get(self, key):
        return self.conn.get(key)

    def delete(self, key):
        return self.conn.delete(key)

    def delete_all(self):
        """
        清空所有Key
        :return:
        """
        return self.conn.flushall()

    def add_set(self, key, *values):
        """
        向指定key中添加值
        :param key:
        :param values:
        :return:
        """
        return self.conn.sadd(key, *values)

    def get_set(self, key):
        """
        获取指定key的Set中的所有数据
        :param key:
        :return:
        """
        return self.conn.smembers(key)

    def is_in_set(self, key, value):
        """
        判断指定key的Set中是否包含value
        :param key:
        :param value:
        :return: boolean => True: 存在; False: 不存在
        """
        return self.conn.sismember(key, value)
