# -*- coding: utf-8 -*-
"""
用户历史听歌记录

@Author YH YR
@Time 2018/10/25 21:57
"""
import json

from scrapy_redis.spiders import RedisCrawlSpider
from CloudMusicSpider.items import UserPlayRecordItem
from CloudMusicSpider.utils.redisUtil import RedisUtil
from CloudMusicSpider.utils.kafkaProducerUtil import KafkaProducerUtil
from CloudMusicSpider.comment.constant import *
from CloudMusicSpider.settings import *


class UserPlayRecordSpider(RedisCrawlSpider):
    name = "UserPlayRecordSpider"
    redis_key = KEY_REQUEST_PLAY_RECORD

    def __init__(self, *a, **kw):
        self.redis_client = RedisUtil(host=REDIS_HOST, port=REDIS_PORT)
        self.kafka_client = KafkaProducerUtil(broker_list)
        super().__init__(*a, **kw)

    def parse(self, response):
        url = response.url
        response_body = json.loads(response.body)
        if response_body['code'] != 200:
            self.redis_client.add_set(KEY_REQUEST_PLAY_RECORD, url)
            raise Exception('user play record: {0} parse error'.format(url))

        user_id = url[url.find('=') + 1: url.find('&')]
        play_records = {'user_id': user_id, 'play_record': response_body['allData']}

        '''
        数据持久化
        Way 1: 格式化写入HDFS的数据格式 -> 每行一条记录
        Way 2: 写入Kafka
        '''
        user_play_record_item = UserPlayRecordItem()
        user_play_record_item['user_play_record'] = json.dumps(play_records) + '\r\n'
        yield user_play_record_item
        # self.kafka_client.produce(TOPIC_USER_PLAY_RECORD_DATA, json.dumps(play_records))
