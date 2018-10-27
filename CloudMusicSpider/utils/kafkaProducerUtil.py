# -*- coding: utf-8 -*-
"""
@Author YH YR
@Time 2018/09/27 14:45
"""
from kafka import KafkaProducer


class KafkaProducerUtil:
    def __init__(self, broker_list):
        self._producer = KafkaProducer(bootstrap_servers=broker_list)

    def produce(self, topic, msg):
        """
        :param topic:
        :param msg: str
        :return:
        """
        self._producer.send(topic, bytes(msg, encoding='utf8'))
        self._producer.flush()
