# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtistInfoListItem(scrapy.Item):
    artist_info_list = scrapy.Field()


class MusicInfoListItem(scrapy.Item):
    song_info_list = scrapy.Field()


class MusicDetailItem(scrapy.Item):
    song_detail = scrapy.Field()


class MusicCommentListItem(scrapy.Item):
    comments = scrapy.Field()


class UserBaseInfoItem(scrapy.Item):
    # 用户信息解析
    # user_id = scrapy.Field()
    # nick_name = scrapy.Field()
    # gender = scrapy.Field()
    # birthday = scrapy.Field()
    # province = scrapy.Field()
    # city = scrapy.Field()
    # auth_status = scrapy.Field()    # 是否经过官方认证 0: 未认证; 1:认证
    # followeds = scrapy.Field()      # 关注数
    # follows = scrapy.Field()        # 粉丝数
    # signature = scrapy.Field()      # 个人签名
    # event_count = scrapy.Field()    # 个人动态数
    # vip_type = scrapy.Field()       # 是否为VIP用户 0: 非VIP用户; 大于0: VIP用户
    # playlist_count = scrapy.Field() # 个人歌单数
    # user_level = scrapy.Field()     # 账号等级
    # listen_songs = scrapy.Field()   # 累计听歌数
    # create_time = scrapy.Field()    # 账号创建时间
    # create_days = scrapy.Field()    # 账号创建距今天数

    # 用户原始数据集
    user_info = scrapy.Field()


class UserFollowInfoItem(scrapy.Item):
    """
    根据不同的使用场景(关注/粉丝), 落库时的字段标识符不同
    关注: follows
    粉丝: followed
    以关注者为例:
        user_id = scrapy.Field()
        nick_name = scrapy.Field()
        follows_user_id = scrapy.Field()
        follows_nick_name = scrapy.Field()
        follows_gender = scrapy.Field()
        follows_vip_type = scrapy.Field()
        follows_followeds = scrapy.Field()
        follows_follows = scrapy.Field()
        follows_event_count = scrapy.Field()
    """
    follow_mapping_list = scrapy.Field()


class UserPlayRecordItem(scrapy.Item):
    user_play_record = scrapy.Field()
