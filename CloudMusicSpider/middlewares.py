# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import time

from CloudMusicSpider.utils.mysqlUtil import MysqlUtil
from CloudMusicSpider.comment.user_agents import agents
from CloudMusicSpider.settings import *


mysql = MysqlUtil(mysql_url, mysql_user, mysql_password, mysql_db_name, mysql_port)


class UserAgentMiddleware(object):
    @staticmethod
    def process_request(request, spider):

        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        request.headers["Referer"] = 'https://music.163.com/'


class ProxyMiddleWare(object):
    """docstring for ProxyMiddleWare"""
    @staticmethod
    def process_request(request, spider):
        proxy = get_random_proxy()
        print("Current request use proxy ip: " + proxy)
        request.meta['proxy'] = proxy

    @staticmethod
    def process_response(request, response, spider):
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            # 增添代理
            proxy = get_random_proxy()
            request.meta['proxy'] = proxy
            return request
        else:
            print("Current proxy ip: {0} is Available".format(request.meta['proxy']))
        return response


# def get_random_proxy():
#     """
#     从本地文件中随机获取IP信息
#     :return:
#     """
#     while 1:
#         with open('./CloudMusicSpider/comment/proxyIp.txt', 'r') as f:
#             proxies = f.readlines()
#         if proxies:
#             break
#         else:
#             time.sleep(1)
#     return random.choice(proxies).strip()

def get_random_proxy():
    """
    从代理IP表中随机获取IP信息
    :return:
    """
    while 1:
        proxy_ip_list = mysql.query('select proxy_ip from proxy_ip_info', num='all')
        if len(proxy_ip_list) > 0:
            return random.choice(proxy_ip_list)[0]
        else:
            time.sleep(1)


class HttpProxyMiddleware(object):
    @staticmethod
    def process_exception(request, exception, spider):
        invalid_ip = request.meta['proxy']
        proxy_id = get_random_proxy()
        request.meta['proxy'] = proxy_id
        print('Target ip: {0} is invalid; Now update proxy ip to try again'.format(invalid_ip, proxy_id))
        return request
