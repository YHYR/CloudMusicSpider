# -*- coding: utf-8 -*-
"""
爬去热门歌手列表,并初始化歌手热门单曲URL
通过在Redis中维护一个artist_id数据集, 保证抽取唯一性

@Author YH YR
@Time 2018/10/17 20:44
"""
import json

from scrapy_redis.spiders import RedisCrawlSpider

from CloudMusicSpider.utils.redisUtil import RedisUtil
from CloudMusicSpider.comment.constant import *
from CloudMusicSpider.settings import *


class HotArtistSpider(RedisCrawlSpider):
    name = "HotArtistSpider"
    redis_key = KEY_REQUEST_START

    def __init__(self, *a, **kw):
        self.redis_client = RedisUtil(host=REDIS_HOST, port=REDIS_PORT)
        super().__init__(*a, **kw)

    def parse(self, response):
        response_body = json.loads(response.body)
        if response_body['code'] != 200:
            self.redis_client.add_set(KEY_REQUEST_START, response.url)
            raise Exception('artist id info: {0} parse error'.format(response.url))

        artist_list = response_body['artists']
        url_doc = set()
        artist_id_doc = set()
        for artist_info in artist_list:
            artist_id = artist_info['id']
            if not self.redis_client.is_in_set(KEY_DATA_ARTIST_ID, artist_id):
                url_doc.add(URL_ARTIST_HOT_SONG.format(artist_id=artist_id))
                artist_id_doc.add(artist_id)

        if len(artist_id_doc) > 0:
            self.redis_client.add_set(KEY_DATA_ARTIST_ID, *artist_id_doc)
        if len(url_doc) > 0:
            self.redis_client.add_set(KEY_REQUEST_SONG_ID, *url_doc)
