# -*- coding: utf-8 -*-
"""
单曲的评论信息

@Author YH YR
@Time 2018/10/20 15:04
"""
import json

from scrapy_redis.spiders import RedisCrawlSpider

from CloudMusicSpider.items import MusicCommentListItem
from CloudMusicSpider.utils.redisUtil import RedisUtil
from CloudMusicSpider.utils.kafkaProducerUtil import KafkaProducerUtil
from CloudMusicSpider.comment.constant import *
from CloudMusicSpider.settings import *


class CommentSpider(RedisCrawlSpider):
    name = "CommentSpider"
    redis_key = KEY_REQUEST_COMMENT

    def __init__(self, *a, **kw):
        self.redis_client = RedisUtil(host=REDIS_HOST, port=REDIS_PORT)
        self.kafka_client = KafkaProducerUtil(broker_list)
        super().__init__(*a, **kw)

    def parse(self, response):
        url = response.url
        response_body = json.loads(response.body)
        if response_body['code'] != 200:
            self.redis_client.add_set(KEY_REQUEST_COMMENT, url)
            raise Exception('comment: {0} parse error'.format(url))

        song_id = url[url.rfind('_') + 1: url.find('?')]
        offset = int(url[url.rfind('=') + 1:])

        url_doc = set()
        user_id_doc = set()
        comments = response_body['comments']
        total_comment_num = response_body['total']
        if len(comments) > 0:
            for comment in comments:
                user_id = comment['user']['userId']
                if not self.redis_client.is_in_set(KEY_DATA_USER_ID, user_id):
                    comment['total_comment_num'] = total_comment_num
                    comment['song_id'] = song_id
                    user_id_doc.add(user_id)
                    # 初始化用户基本信息URL
                    url_doc.add(URL_USER_BASE_INFO.format(user_id=comment['user']['userId']))
                    '''数据持久化 写入Kafka'''
                    # self.kafka_client.produce(TOPIC_COMMENT_DATA, json.dumps(comment))

            if len(user_id_doc) > 0:
                self.redis_client.add_set(KEY_DATA_USER_ID, *user_id_doc)
            if len(url_doc) > 0:
                self.redis_client.add_set(KEY_REQUEST_USER_INFO, *url_doc)

            '''数据持久化 格式化写入HDFS的数据格式 -> 每行一条记录'''
            music_review_list_item = MusicCommentListItem()
            format_comments = map(lambda x: json.dumps(x), comments)
            music_review_list_item['comments'] = '\r\n'.join(format_comments)
            yield music_review_list_item

            if offset <= total_comment_num:
                offset = offset + DATA_LIMIT
                base_url = URL_COMMENT.format(song_id=song_id, limit=DATA_LIMIT, offset=offset)
                self.redis_client.add_set(KEY_REQUEST_COMMENT, base_url)
