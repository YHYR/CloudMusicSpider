# -*- coding: utf-8 -*-

# Scrapy settings for CloudMusicSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'CloudMusicSpider'

SPIDER_MODULES = ['CloudMusicSpider.spiders']
NEWSPIDER_MODULE = 'CloudMusicSpider.spiders'

COMMANDS_MODULE = 'CloudMusicSpider.commands'

'''
Scrapy-redis Setting
'''
# scrapy-redis去重组件
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# scrapy-redis调度器组件
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 允许暂停，redis请求记录不丢失
SCHEDULER_PERSIST = True

'''
scrapy-redis请求队列形式
1,按优先级: scrapy_redis.queue.SpiderPriorityQueue
2,队列形式: scrapy_redis.queue.SpiderQueue
3，栈形式:  scrapy_redis.queue.SpiderStack
'''
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# redis中保存请求url的数据类型
REDIS_START_URLS_AS_SET = True


'''
Scrapy Setting
'''
DOWNLOADER_MIDDLEWARES = {
    'CloudMusicSpider.middlewares.UserAgentMiddleware': 401,
    # 代理设置
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 850,
    # 'CloudMusicSpider.middlewares.HttpProxyMiddleware': 543,
    # 'CloudMusicSpider.middlewares.ProxyMiddleWare': 545,
}

ITEM_PIPELINES = {
    'CloudMusicSpider.pipelines.CloudMusicPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400
}

# 禁用重定向 => 暂时消除会访问非目标地址的情况; 具体原因不详
REDIRECT_ENABLED = False

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


'''
Custom Setting
'''
# Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# HDFS
HDFS_URL = 'http://localhost:50070'

# Kafka
broker_list = 'localhost:9092'

# MySQL
mysql_url = 'localhost'
mysql_user = 'root'
mysql_password = 'root'
mysql_port = 3306
mysql_db_name = 'cloud_music_db'
