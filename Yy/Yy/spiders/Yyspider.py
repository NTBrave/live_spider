# -*- coding: utf-8 -*-
import scrapy,re,json,time
from scrapy.http import Request
from Yy.items import YyItem
from runspider import spidertime
# from runspider import Runtime
class YyspiderSpider(scrapy.Spider):
    name = 'yy'
    allowed_domains = ['www.yy.com']#设置爬虫允许抓取的
    start_urls = ['http://www.yy.com/catalog']#设置第一个爬取的url
    allow_pagenum = 5;   #设置爬取频道的数量
    total_pagenum = 1;   #计算档前已爬取频道的数量
    url_dict={}       #设置存放url的dict
    timetime = spidertime()  # 实例化时间专用类
    items_time = timetime.get_time()  # 记录爬取时间
    def parse(self, response):#获取所有频道的url 、频道id  、频道名称
        parse_content = response.xpath('//div[@class="w-video-module-cataloglist"]//li')  # 抓取当前频道
        for i in parse_content:
            channel_title = i.xpath('a[@class="box"]/span[@class="t"]/text()').extract_first()  # 抓取频道名称
            channel_url = i.xpath('a[@class="box"]/@href').extract_first()  # 抓取当前频道url
            #构造ajax请求地址的信息，原网址有可能会改，具体情况请自行维护
            if(channel_url == '/dancing'):
                channel_biz = 'dance'
                channel_subBiz = 'idx'
                channel_moduleId = '313'
                channel_pageSize = '24'
            elif channel_url == '/music/':
                channel_biz = 'sing'
                channel_subBiz = 'idx'
                channel_moduleId = '308'
                channel_pageSize = '60'
            elif channel_url == '/show/':
                channel_biz = 'talk'
                channel_subBiz = 'idx'
                channel_moduleId = '328'
                channel_pageSize = '60'
            elif channel_url == '/travel/lvyou':
                channel_biz = 'red'
                channel_subBiz = 'lvyou'
                channel_moduleId = '560'
                channel_pageSize = '22'
            elif channel_url == '/chicken/jdqs':
                channel_biz = 'chicken'
                channel_subBiz = 'jdqs'
                channel_moduleId = '1473'
                channel_pageSize = '60'
            else:
                channel_biz = '0'
                channel_subBiz = '0'
                channel_moduleId = '0'
                channel_pageSize = '0'

            channel_url = 'http://www.yy.com/' + channel_url
            channel_data = {"url": channel_url, "channel_biz": channel_biz, "channel_subBiz":channel_subBiz,
                            "channel_moduleId":channel_moduleId, "channel_pageSize":channel_pageSize}
            if self.total_pagenum <= self.allow_pagenum:  # 用于控制爬出抓取数量，当total_pagenum小于allow_pagenum 继续爬
                self.total_pagenum += 1
                yield Request(url=channel_url, meta={'channel_data': channel_data, 'channel': channel_title},
                              callback=self.channel_get)
                # 使用request，meta携带数据，回调函数为channel_get

    def channel_get(self, response):
        #def parse的回调函数，根据channel_data构造主播数据连接并执行请求
        page_nums = response.xpath('/html/body/script[7]').re(r'\d+\.?\d*')
        page_num = int(page_nums[0])
        # 抓取当前频道一共有多少页，并转为int格式
        channel_biz = response.meta['channel_data']['channel_biz']  #用于构造url从而实现翻页
        channel_subBiz = response.meta['channel_data']['channel_subBiz']
        channel_moduleId = response.meta['channel_data']['channel_moduleId']
        channel_pageSize = response.meta['channel_data']['channel_pageSize']
        channel = response.meta['channel']  # 将传入的meta的dict中的channel值赋给channel
        for i in range(1, page_num + 1):  # 根据page_num数量构造"下一页"并继续抓取，这个构造的网站要自己找的
            url = 'http://www.yy.com/more/page.action?biz={biz}&subBiz={subBiz}&page={page}&moduleId={moduleId}&pageSize={pageSize}'.format(
                page=i, biz=channel_biz, subBiz=channel_subBiz, moduleId=channel_moduleId, pageSize=channel_pageSize)
            # 获取下一页的json数据
            yield Request(url=url, meta={'page': i, 'channel': channel},
                          callback=self.channel_parse)  # meta携带数据为频道当前页码，频道名称，回调函数为channel_parse

    def channel_parse(self, response):
        #channel_get 的回调函数，根据返回的json数据抓取相应内容，并抓出主播的房间链接，对房间链接执行请求
        response_json = json.loads(response.text)  # 利用json.loads将json数据转为字典
        channel = response.meta['channel']
        for i in response_json['data']['data']:
            items = YyItem()  # 实例化item.HuyaItem
            items['channel'] = channel  # 获取频道名称
            items['watch_num'] = int(i['users'])  # 获取观看数量 设置为整数方便排序
            items['anchor_roomname'] = i['desc']  # 获取房间名称
            items['anchor_url'] = 'http://www.yy.com/' + i['liveUrl']
            items['anchor_name'] = i['name']  # 获主播名称
            yield Request(url=items['anchor_url'], meta={'items': items},
                          callback=self.room_parse)
            # 进入主播房间url获取主播订阅数量，meta携带数据为刚抓取的items，回调函数为room_parse

    def room_parse(self, response):
        items = response.meta['items']
        #下面是获取关注的人数，暂时只能去script里面拿，还要正则处理一下，
        items['fan_num'] = response.xpath('/html/body/script[3]').extract()
        s = str(items['fan_num'])
        p = re.compile(r'(?:numOfFun: ")\d*')
        sss = re.findall(r'\d+', "  ".join(re.findall(p, s)))
        if(sss==[]):
            sss[0] = 0
        items['fan_num'] = sss[0]
        items['crawl_time'] = self.items_time  # 记录爬取时间
        yield items  # 输出items
