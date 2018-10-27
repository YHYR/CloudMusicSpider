# -*- coding: utf-8 -*-
"""
单曲的详情信息

@Author YH YR
@Time 2018/10/25 21:27
"""
import json

from scrapy_redis.spiders import RedisCrawlSpider
from CloudMusicSpider.items import MusicDetailItem
from CloudMusicSpider.utils.redisUtil import RedisUtil
from CloudMusicSpider.utils.kafkaProducerUtil import KafkaProducerUtil
from CloudMusicSpider.comment.constant import *
from CloudMusicSpider.settings import *


class SongDetailSpider(RedisCrawlSpider):
    name = "SongDetailSpider"
    redis_key = KEY_REQUEST_SONG_DETAIL

    def __init__(self, *a, **kw):
        self.redis_client = RedisUtil(host=REDIS_HOST, port=REDIS_PORT)
        self.kafka_client = KafkaProducerUtil(broker_list)
        super().__init__(*a, **kw)

    def parse(self, response):
        response_body = json.loads(response.body)
        if response_body['code'] != 200:
            self.redis_client.add_set(KEY_REQUEST_SONG_DETAIL, response.url)
            raise Exception('song detail: {0} parse error'.format(response.url))

        song_detail = response_body['songs'][0]

        '''
        数据持久化
        Way 1: 格式化写入HDFS的数据格式 -> 每行一条记录
        Way 2: 写入Kafka
        '''
        music_detail_item = MusicDetailItem()
        music_detail_item['song_detail'] = json.dumps(song_detail) + '\r\n'
        yield music_detail_item
        # self.kafka_client.produce(TOPIC_SONG_DETAIL_DATA, json.dumps(song_detail))
