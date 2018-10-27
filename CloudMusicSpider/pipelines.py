# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from CloudMusicSpider.items import MusicCommentListItem, MusicDetailItem, ArtistInfoListItem, \
    UserBaseInfoItem, UserFollowInfoItem, UserPlayRecordItem
from CloudMusicSpider.utils.hdfsUtil import HDFSUtil
from CloudMusicSpider.utils.kafkaProducerUtil import KafkaProducerUtil
from CloudMusicSpider.settings import *
from CloudMusicSpider.comment.constant import *


class CloudMusicPipeline(object):
    def __init__(self):
        self.hdfs_client = HDFSUtil(HDFS_URL)

    def process_item(self, item, spider):
        if isinstance(item, ArtistInfoListItem):
            pass

        if isinstance(item, MusicDetailItem):
            self.hdfs_client.write_to_hdfs(FILE_SONG_DETAIL_DATA_PATH, item['song_detail'])

        if isinstance(item, MusicCommentListItem):
            self.hdfs_client.write_to_hdfs(FILE_COMMENT_DATA_PATH, item['comments'])

        if isinstance(item, UserBaseInfoItem):
            self.hdfs_client.write_to_hdfs(FILE_USER_BASE_INFO_DATA_PATH, item['user_info'])

        if isinstance(item, UserFollowInfoItem):
            if 'follows_user_id' in item['follow_mapping_list']:
                self.hdfs_client.write_to_hdfs(FILE_FOLLOWS_DATA_PATH, item['follow_mapping_list'])
            elif 'followed_user_id' in item['follow_mapping_list']:
                self.hdfs_client.write_to_hdfs(FILE_FOLLOWED_DATA_PATH, item['follow_mapping_list'])
            else:
                pass

        if isinstance(item, UserPlayRecordItem):
            self.hdfs_client.write_to_hdfs(FILE_USER_PLAY_RECORD_DATA_PATH, item['user_play_record'])
