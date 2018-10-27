# -*- coding: utf-8 -*-
"""
@Author YH YR
@Time 2018/10/22 20:30
"""

INIT_OFFSET = 0
DATA_LIMIT = 100

"""
Redis Key
"""
# Request Key
KEY_REQUEST_START = 'CloudMusic_Request:start_urls'
KEY_REQUEST_SONG_ID = 'CloudMusic_Request:song_urls'
KEY_REQUEST_SONG_DETAIL = 'CloudMusic_Request:song_detail_urls'
KEY_REQUEST_COMMENT = 'CloudMusic_Request:comment_urls'
KEY_REQUEST_USER_INFO = 'CloudMusic_Request:user_info_urls'
KEY_REQUEST_FOLLOWED = 'CloudMusic_Request:followed_urls'
KEY_REQUEST_FOLLOWS = 'CloudMusic_Request:follows_urls'
KEY_REQUEST_PLAY_RECORD = 'CloudMusic_Request:play_record_urls'

# Data Key
KEY_DATA_ARTIST_ID = 'CloudMusic_Data:artist_id'
KEY_DATA_SONG_ID = 'CloudMusic_Data:song_id'
KEY_DATA_USER_ID = 'CloudMusic_Data:user_id'
KEY_DATA_USER_FOLLOW = 'CloudMusic_Data:user_follow_info:{user_id}'


"""
HDFS Data File PATH
"""
FILE_SONG_DETAIL_DATA_PATH = '/cloud_music_data/songDetailData.json'
FILE_COMMENT_DATA_PATH = '/cloud_music_data/commentData.json'
FILE_USER_BASE_INFO_DATA_PATH = '/cloud_music_data/userData.json'
FILE_FOLLOWS_DATA_PATH = '/cloud_music_data/userFollowsData.json'
FILE_FOLLOWED_DATA_PATH = '/cloud_music_data/userFollowedsData.json'
FILE_USER_PLAY_RECORD_DATA_PATH = '/cloud_music_data/userPlayRecordData.json'


"""
Kafka Topic
"""
TOPIC_SONG_DETAIL_DATA = 'cloud_music_song_detail'
TOPIC_COMMENT_DATA = 'cloud_music_comment'
TOPIC_USER_BASE_INFO_DATA = 'cloud_music_user_base_info'
TOPIC_USER_FOLLOWS_DATA = 'cloud_music_user_follows'
TOPIC_USER_FOLLOWEDS_DATA = 'cloud_music_user_followeds'
TOPIC_USER_PLAY_RECORD_DATA = 'cloud_music_user_play_record'


"""
Cloud Music DATA API 
"""
# 热门歌手
URL_HOT_ARTIST = 'http://music.163.com/api/artist/top?offset=0&limit=100&total=false'

# 歌手简介 【暂未使用】
URL_ARTIST_INTRODUCTION = 'http://music.163.com/api/artist/introduction?id={artist_id}'

# 歌手热门单曲
URL_ARTIST_HOT_SONG = 'http://music.163.com/api/v1/artist/{artist_id}'

# 单曲详情
URL_SONG_DETAIL_INFO = 'http://music.163.com/api/song/detail/?id={id}&ids=[{ids}]'

# 评语
URL_COMMENT = 'https://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit={limit}&offset={offset}'

# 用户基本
URL_USER_BASE_INFO = 'http://music.163.com/api/v1/user/detail/{user_id}'

# 用户粉丝
URL_USER_FOLLOWED = 'http://music.163.com/api/user/getfolloweds?userId={user_id}&limit={limit}&offset={offset}'

# 用户关注
URL_USER_FOLLOWS = 'http://music.163.com/api/user/getfollows/{user_id}?limit={limit}&offset={offset}'

# 用户历史听歌记录 type => 0:代表所有听过的各(最多100首); 1:代表最近一周
URL_USER_PLAY_RECORD = 'http://music.163.com/api/v1/play/record?uid={user_id}&type=0'
