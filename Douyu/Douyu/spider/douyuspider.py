# -*- coding: utf-8 -*-
import scrapy, re,json,time
from scrapy.http import Request
from Douyu.items import DouyuItem
from runspider import spidertime


class douyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['www.douyu.com']
    start_urls = ['http://www.douyu.com/g_LOL',
                  'http://www.douyu.com/g_jdqs',
                  'http://www.douyu.com/g_wzry',
                  'http://www.douyu.com/g_DNF',
                  'http://www.douyu.com/g_TVgame']
    allow_pagenum = 5;
    total_pagenum = 1;
    url_dict={}
    timetime = spidertime()  # 实例化时间专用类
    items_time = timetime.get_time()  # 记录爬取时间


    def parse(self, response):
        channel_title = response.xpath('//h2[@class="layout-Partition-title"]/text()') .extract_first()
        page_msg = response.xpath('/html/body/script[2]') .extract_first()
        p = re.compile(r'(?:pageCount":)\d*')
        pageCount = re.findall(r'\d+', "  ".join(re.findall(p, page_msg)))
        pages = int(pageCount[0])
        if channel_title == '英雄联盟':
            url_list = '/2_1/'
        elif channel_title == '绝地求生':
            url_list = '/2_270/'
        elif channel_title == '王者荣耀':
            url_list = '/2_181/'
        elif channel_title == '主机游戏':
            url_list = '/2_19/'
        elif channel_title == 'DNF':
            url_list = '/2_40/'
        else:
            url_list = '/2_1/'
        # print(channel_title, pages, url_list)
        for i in range(1, pages+1):
            url = 'http://www.douyu.com/gapi/rkc/directory{url_list}{pagei}'.format(pagei=i, url_list=url_list)
            yield Request(url=url, meta={'page': i, 'channel': channel_title}, callback=self.channel_parse)

    def channel_parse(self, response):
        #channel_get 的回调函数，根据返回的json数据抓取相应内容，并抓出主播的房间链接，对房间链接执行请求
        response_json = json.loads(response.text)  # 利用json.loads将json数据转为字典
        channel = response.meta['channel']
        for i in response_json['data']['rl']:
            items = DouyuItem()  # 实例化item.HuyaItem
            items['channel'] = channel  # 获取频道名称
            items['watch_num'] = int(i['ol'])  # 获取观看数量 设置为整数方便排序
            items['anchor_roomname'] = i['rn']  # 获取房间名称 加密的
            items['anchor_url'] = 'http://www.douyu.com' + i['url']
            items['anchor_name'] = i['nn']  # 获主播名称 加密的
            yield Request(url=items['anchor_url'], meta={'items': items},
                          callback=self.room_parse)#重跳转问题修复, dont_filter=True
            # 进入主播房间url获取主播订阅数量，meta携带数据为刚抓取的items，回调函数为room_parse

    def room_parse(self, response):
        items = response.meta['items']
        items['fan_num'] = items['watch_num']
        items['crawl_time'] = self.items_time  # 记录爬取时间
        yield items  # 输出items
