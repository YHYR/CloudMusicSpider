# -*- coding: utf-8 -*-
"""
歌手的热门单曲

@Author YH YR
@Time 2018/10/17 19:38
"""
import json

from scrapy_redis.spiders import RedisCrawlSpider
from CloudMusicSpider.utils.redisUtil import RedisUtil
from CloudMusicSpider.comment.constant import *
from CloudMusicSpider.settings import *


class SongIdSpider(RedisCrawlSpider):
    name = "SongIdSpider"
    redis_key = KEY_REQUEST_SONG_ID

    def __init__(self, *a, **kw):
        self.redis_client = RedisUtil(host=REDIS_HOST, port=REDIS_PORT)
        super().__init__(*a, **kw)

    def parse(self, response):
        response_body = json.loads(response.body)
        if response_body['code'] != 200:
            self.redis_client.add_set(KEY_REQUEST_SONG_ID, response.url)
            raise Exception('song list: {0} parse error', response.url)

        hot_song_list = response_body['hotSongs']
        song_id_doc = set()
        song_detail_url_doc = set()
        comment_url_doc = set()
        for hot_song in hot_song_list:
            song_id = hot_song['id']
            if not self.redis_client.is_in_set(KEY_DATA_SONG_ID, song_id):
                song_id_doc.add(song_id)
                # 初始化单曲详情URL
                song_detail_url_doc.add(URL_SONG_DETAIL_INFO.format(id=song_id, ids=song_id))
                # 初始化单曲评论URL
                comment_url_doc.add(URL_COMMENT.format(song_id=song_id, limit=DATA_LIMIT, offset=INIT_OFFSET))

        if len(song_id_doc) > 0:
            self.redis_client.add_set(KEY_DATA_SONG_ID, *song_id_doc)
        if len(comment_url_doc) > 0:
            self.redis_client.add_set(KEY_REQUEST_COMMENT, *comment_url_doc)
        if len(song_detail_url_doc) > 0:
            self.redis_client.add_set(KEY_REQUEST_SONG_DETAIL, *song_detail_url_doc)
