# -*- coding: utf-8 -*-
"""
用户的关注者信息

@Author YH YR
@Time 2018/10/20 21:11
"""
import json

from scrapy_redis.spiders import RedisCrawlSpider

from CloudMusicSpider.items import UserFollowInfoItem
from CloudMusicSpider.utils.redisUtil import RedisUtil
from CloudMusicSpider.utils.kafkaProducerUtil import KafkaProducerUtil
from CloudMusicSpider.comment.constant import *
from CloudMusicSpider.settings import *


class FollowsSpider(RedisCrawlSpider):
    name = "FollowsSpider"
    redis_key = KEY_REQUEST_FOLLOWS

    def __init__(self, *a, **kw):
        self.redis_client = RedisUtil(host=REDIS_HOST, port=REDIS_PORT)
        self.kafka_client = KafkaProducerUtil(broker_list)
        super().__init__(*a, **kw)

    def parse(self, response):
        url = response.url
        response_body = json.loads(response.body)
        if response_body['code'] != 200:
            self.redis_client.add_set(KEY_REQUEST_FOLLOWS, url)
            raise Exception('follows: {0} parse error'.format(url))

        user_id = url[url.rfind('/') + 1: url.find('?')]
        offset = int(url[url.rfind('=') + 1:])

        if len(response_body['follow']) > 0:
            data_doc = []
            user_id_doc = set()
            follows_user_url_doc = set()
            for follows_info in response_body['follow']:
                # 解析用户关注者数据
                follows_user_id = follows_info['userId']
                dic = {'user_id': user_id, 'follows_user_id': follows_info['userId'],
                       'follows_nick_name': follows_info['nickname'], 'follows_gender': follows_info['gender'],
                       'follows_vip_type': follows_info['vipType'], 'follows_followeds': follows_info['followeds'],
                       'follows_follows': follows_info['follows'], 'follows_event_count': follows_info['eventCount']}
                data_doc.append(dic)
                '''数据持久化 写入Kafka'''
                # self.kafka_client.produce(TOPIC_USER_FOLLOWS_DATA, json.dumps(dic))

                # 深度爬去用户信息 根据user_id数据集规避重复爬取
                if not self.redis_client.is_in_set(KEY_DATA_USER_ID, follows_user_id):
                    follows_user_url_doc.add(URL_USER_BASE_INFO.format(user_id=follows_user_id))
                    user_id_doc.add(follows_user_id)

            if len(user_id_doc) > 0:
                self.redis_client.add_set(KEY_DATA_USER_ID, *user_id_doc)
            if len(follows_user_url_doc) > 0:
                self.redis_client.add_set(KEY_REQUEST_USER_INFO, *follows_user_url_doc)

            '''数据持久化 格式化写入HDFS的数据格式 -> 每行一条记录'''
            if len(data_doc) > 0:
                # 格式化写入HDFS的数据格式 -> 每行一条记录
                user_follows_info_item = UserFollowInfoItem()
                format_follows_data = map(lambda x: json.dumps(x), data_doc)
                user_follows_info_item['follow_mapping_list'] = '\r\n'.join(format_follows_data)
                yield user_follows_info_item

            # 爬取所有的关注者
            user_follow_info_dic = json.loads(self.redis_client.get(KEY_DATA_USER_FOLLOW.format(user_id=user_id)))
            if offset <= user_follow_info_dic['follows']:
                offset = offset + DATA_LIMIT
                user_follows_url = URL_USER_FOLLOWS.format(user_id=user_id, offset=offset, limit=DATA_LIMIT)
                self.redis_client.add_set(KEY_REQUEST_FOLLOWS, user_follows_url)
