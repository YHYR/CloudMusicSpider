# -*- coding: utf-8 -*-
"""
用户的基本信息

@Author YH YR
@Time 2018/10/20 16:52
"""
import json

from scrapy_redis.spiders import RedisCrawlSpider

from CloudMusicSpider.items import UserBaseInfoItem
from CloudMusicSpider.utils.redisUtil import RedisUtil
from CloudMusicSpider.utils.kafkaProducerUtil import KafkaProducerUtil
from CloudMusicSpider.comment.constant import *
from CloudMusicSpider.settings import *


class UserInfoSpider(RedisCrawlSpider):
    name = "UserInfoSpider"
    redis_key = KEY_REQUEST_USER_INFO

    def __init__(self, *a, **kw):
        self.redis_client = RedisUtil(host=REDIS_HOST, port=REDIS_PORT)
        self.kafka_client = KafkaProducerUtil(broker_list)
        super().__init__(*a, **kw)

    def parse(self, response):
        response_body = json.loads(response.body)
        if response_body['code'] != 200:
            self.redis_client.add_set(KEY_REQUEST_USER_INFO, response.url)
            raise Exception('user base info: {0} parse error'.format(response.url))

        # 解析用户基本信息
        user_id = response_body['profile']['userId']
        followeds = response_body['profile']['followeds']
        follows = response_body['profile']['follows']

        # 持久化用户的关注、粉丝人数映射
        user_follow_info_dic = {'user_id': user_id, 'followeds': followeds, 'follows': follows}
        self.redis_client.set(KEY_DATA_USER_FOLLOW.format(user_id=user_id), json.dumps(user_follow_info_dic))

        # 初始化关注者列表URL
        self.redis_client.add_set(KEY_REQUEST_FOLLOWS,
                                  URL_USER_FOLLOWS.format(user_id=user_id, limit=DATA_LIMIT, offset=INIT_OFFSET))
        # 初始化粉丝列表URL
        self.redis_client.add_set(KEY_REQUEST_FOLLOWED,
                                  URL_USER_FOLLOWED.format(user_id=user_id, limit=DATA_LIMIT, offset=INIT_OFFSET))

        # 初始化用户听歌记录URL
        self.redis_client.add_set(KEY_REQUEST_PLAY_RECORD, URL_USER_PLAY_RECORD.format(user_id=user_id))

        '''
        数据持久化
        Way 1: 格式化写入HDFS的数据格式 -> 每行一条记录
        Way 2: 写入Kafka
        '''
        user_base_info_item = UserBaseInfoItem()
        user_base_info_item['user_info'] = json.dumps(response_body) + '\r\n'
        yield user_base_info_item
        # self.kafka_client.produce(TOPIC_USER_BASE_INFO_DATA, response.body)
