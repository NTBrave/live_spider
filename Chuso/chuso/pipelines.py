# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, codecs
import pymongo

class ChusoPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)  # 创建mongodb连接
        db = client['spiderData']  # 创建mongodb数据库
        self.collection = db['chusoanchor']  # 创建数据库中collection

    def process_item(self, item, spider):
        item = dict(item)  # 将抓到的item转为dict格式
        self.collection.insert(item)  # 将item写进mongodb中

