# 网易云音乐分布式爬虫

# 功能

基于Scrapy-redis爬取网易云音乐的歌手、歌曲(基本信息、评论信息)、用户(基本信息、关注者、粉丝、听歌记录)数据，并持久化到HDFS(or Kafka)。

实现数据爬取的唯一性校验和用户的深度挖掘；详见[博客](https://yhyr.github.io/)

【后续会基于此做数据分析】

## 依赖

> Python 3
>
> scrapy_redis
>
> redis
>
> mysql-python
>
> kafka-python
>
> hdfs

*以上依赖通过pip install xx 直接安装即可*

# 网易云音乐API汇总

## 热门歌手

> http://music.163.com/api/artist/top?limit={limit}&offset={offset}&total=false
>
> 需要设置User-Agent、Referer; 默认只能获取100位热门歌手

`curl -A "Mozilla/2.02E (Win95; U)" -e "http://music.163.com" "http://music.163.com/api/artist/top?limit=100&offset=0&total=false"`

## 歌手简介

> http://music.163.com/api/artist/introduction?id={artist_id}
>
> 需要设置User-Agent、Referer;

`curl -A "Mozilla/2.02E (Win95; U)" -e "http://music.163.com" "http://music.163.com/api/artist/introduction?id=5781"`

## 歌手热门单曲

> http://music.163.com/api/v1/artist/{artist_id}
>
> 需要设置User-Agent、Referer

`curl -A "Mozilla/2.02E (Win95; U)" -e "http://music.163.com" "http://music.163.com/api/v1/artist/5781"`

## 单曲信息

> http://music.163.com/api/song/detail/?id={song_id}&ids=[{song_id}]

`curl "http://music.163.com/api/song/detail/?id=32507038&ids=\[32507038\]"`

## 歌词信息

> http://music.163.com/api/song/lyric?os=pc&id={song_id}&lv=-1&kv=-1&tv=-1

`curl "http://music.163.com/api/song/lyric?os=pc&id=32507038&lv=-1&kv=-1&tv=-1"`

## 单曲评论信息

> https://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit={limit}&offset={offset}
>
> 去掉url中的v1地址同样有效

`curl "https://music.163.com/api/v1/resource/comments/R_SO_4_32507038?offset=0&limit=100"`

## 歌单信息

> http://music.163.com/api/playlist/detail?id={playlist_id}

`curl "http://music.163.com/api/playlist/detail?id=2359934198"`

## 专辑信息

> http://music.163.com/api/album/{album_id}

`curl "http://music.163.com/api/album/3154175"`

## 用户主页信息

> http://music.163.com/api/v1/user/detail/{user_home_id}

`curl "http://music.163.com/api/v1/user/detail/62326994"`

## 用户粉丝信息

> http://music.163.com/api/user/getfolloweds?userId={user_id}&limit={limit}&offset={offset}

`curl "http://music.163.com/api/user/getfolloweds?userId=62326994&limit=100&offset=0"`

## 用户关注者信息

> http://music.163.com/api/user/getfollows/{user_id}?limit={limit}&offset={offset}

`curl "http://music.163.com/api/user/getfollows/62326994?limit=100&offset=0"`

## 用户听歌记录

> http://music.163.com/api/v1/play/record?uid={user_id}&type={type}
>
> type => 0: all(如果大于100, 取前一百); 1: week

`curl "http://music.163.com/api/v1/play/record?uid=68329420&type=0"`

*API中涉及到的limit最大有效值为100*

## 答谢

感谢[sqaiyan](https://github.com/sqaiyan/netmusic-node)在数据API上给予的灵感

感谢[LiuXingMing](https://github.com/LiuXingMing/SinaSpider)在分布式爬虫实现上给予的灵感