# -*- coding: utf-8 -*-
"""
用户的粉丝信息

@Author YH YR
@Time 2018/10/21 11:24
"""
import json

from scrapy_redis.spiders import RedisCrawlSpider

from CloudMusicSpider.items import UserFollowInfoItem
from CloudMusicSpider.utils.redisUtil import RedisUtil
from CloudMusicSpider.utils.kafkaProducerUtil import KafkaProducerUtil
from CloudMusicSpider.comment.constant import *
from CloudMusicSpider.settings import *


class FollowedSpider(RedisCrawlSpider):
    name = "FollowedSpider"
    redis_key = KEY_REQUEST_FOLLOWED

    def __init__(self, *a, **kw):
        self.redis_client = RedisUtil(host=REDIS_HOST, port=REDIS_PORT)
        self.kafka_client = KafkaProducerUtil(broker_list)
        super().__init__(*a, **kw)

    def parse(self, response):
        url = response.url
        response_body = json.loads(response.body)
        if response_body['code'] != 200:
            self.redis_client.add_set(KEY_REQUEST_FOLLOWED, url)
            raise Exception('followed: {0} parse error'.format(url))

        user_id = url[url.find('=') + 1: url.find('&')]
        offset = int(url[url.rfind('=') + 1:])

        if len(response_body['followeds']) > 0:
            data_doc = []
            user_id_doc = set()
            followed_user_url_doc = set()
            for followed_info in response_body['followeds']:
                # 解析用户粉丝数据
                followed_user_id = followed_info['userId']
                dic = {'user_id': user_id, 'followed_user_id': followed_user_id,
                       'followed_nick_name': followed_info['nickname'], 'followed_gender': followed_info['gender'],
                       'followed_vip_type': followed_info['vipType'], 'followed_followeds': followed_info['followeds'],
                       'followed_follows': followed_info['follows'],
                       'followed_event_count': followed_info['eventCount']}
                data_doc.append(dic)
                '''数据持久化 写入Kafka'''
                # self.kafka_client.produce(TOPIC_USER_FOLLOWEDS_DATA, json.dumps(dic))

                # 深度爬去用户信息 根据user_id数据集规避重复爬取
                if not self.redis_client.is_in_set(KEY_DATA_USER_ID, followed_user_id):
                    followed_user_url_doc.add(URL_USER_BASE_INFO.format(user_id=followed_user_id))
                    user_id_doc.add(followed_user_id)
            if len(user_id_doc) > 0:
                self.redis_client.add_set(KEY_DATA_USER_ID, *user_id_doc)
            if len(followed_user_url_doc) > 0:
                self.redis_client.add_set(KEY_REQUEST_USER_INFO, *followed_user_url_doc)

            '''数据持久化 格式化写入HDFS的数据格式 -> 每行一条记录'''
            if len(data_doc) > 0:
                # 格式化写入HDFS的数据格式 -> 每行一条记录
                user_follows_info_item = UserFollowInfoItem()
                format_followed_data = map(lambda x: json.dumps(x), data_doc)
                user_follows_info_item['follow_mapping_list'] = '\r\n'.join(format_followed_data)
                yield user_follows_info_item

            # 爬取所有的粉丝
            user_follow_info_dic = json.loads(self.redis_client.get(KEY_DATA_USER_FOLLOW.format(user_id=user_id)))
            if offset <= user_follow_info_dic['followeds']:
                offset = offset + DATA_LIMIT
                user_followed_url = URL_USER_FOLLOWED.format(user_id=user_id, limit=DATA_LIMIT, offset=offset)
                self.redis_client.add_set(KEY_REQUEST_FOLLOWED, user_followed_url)
