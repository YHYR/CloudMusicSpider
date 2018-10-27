# -*- coding: utf-8 -*-
"""
@Author YH YR
@Time 2018/10/02 16:09
"""
import MySQLdb


class MysqlUtil:
    def __init__(self, host, user, pass_wd, db, port):
        self.__host = host
        self.__user = user
        self.__pass_wd = pass_wd
        self.__db = db
        self.__port = int(port)
        self.__connection = None

    def __del__(self):
        if self.__connection and self.__connection.open:
            self.__connection.close()

    def __get_connection(self):
        if self.__connection is None or (self.__connection.open != 1):
            self.__connection = MySQLdb.connect(host=self.__host, user=self.__user, passwd=self.__pass_wd, db=self.__db, port=self.__port, charset='utf8')
        try:
            self.__connection.ping()
        except:
            self.__connection = MySQLdb.connect(host=self.__host, user=self.__user, passwd=self.__pass_wd, db=self.__db, port=self.__port, charset='utf8')
        return self.__connection

    def query(self, sql, num=1):
        conn = self.__get_connection()
        cur = conn.cursor()

        cur.execute(sql)
        ret = cur.fetchall()
        conn.commit()
        if ret == 0:
            ret = []
        else:
            record_len = len(ret)
            if (num == 'all') or (num >= record_len):
                ret = ret
            else:
                ret = ret[0:num]
        cur.close()
        return ret

    def modify(self, sql):
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()


if __name__ == '__main__':
    mysql = MysqlUtil('localhost', 'root', 'root', 'test', 3306)
    result = mysql.query("select pass_word from demo", num='all')
    import random
    temp = random.choice(result)[0]
    pass