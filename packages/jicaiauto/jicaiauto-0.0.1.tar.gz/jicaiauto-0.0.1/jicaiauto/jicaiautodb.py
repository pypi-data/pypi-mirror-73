#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiTools'
__script__ = 'init_db.py'
__create_time__ = '2020/7/2 21:45'

from sqlite3 import connect
from os import path

class DB(object):
    def __init__(self):
        self.conn = connect(path.dirname(path.abspath(__file__)) + '/jicaiauto.db')
        self.cur = self.conn.cursor()

    def select(self, sql=None, parames=None, *args, **kwargs):
        return self.cur.execute(sql).fetchall()

    def update(self, sql=None, parames=None, *args, **kwargs):
        self.cur.execute(sql)
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()