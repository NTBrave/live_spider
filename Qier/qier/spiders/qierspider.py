import scrapy,re,json,time
from scrapy.http import Request
from qier.items import QierItem
from runspider import spidertime

class qierSpider(scrapy.Spider):
    name = 'qier'
    allowed_domains = ['egame.qq.com']  # 设置爬虫允许抓取的
    start_urls = ['http://egame.qq.com/gamelist']  # 设置第一个爬取的url
    allow_pagenum = 5;  # 设置爬取频道的数量
    total_pagenum = 1;  # 计算档前已爬取频道的数量
    url_dict = {}  # 设置存放url的dic
    timetime = spidertime()#实例化时间专用类
    items_time = timetime.get_time()  # 记录爬取时间
    def parse(self, response):
        # parse_content = response.xpath('//div[@class="gui-main"]/ul[2]/li')  # 抓取当前频道
        for i in response.xpath('//div[@class="gui-main"]/ul[2]/li'):
            channel_title = i.xpath('a/p/text()').extract()  # 抓取频道名称
            channel_title =channel_title[0]
            channel_url = 'https://egame.qq.com' + i.xpath('a/@href').extract_first()  # 抓取当前频道url
            if self.total_pagenum <= self.allow_pagenum:  # 用于控制爬出抓取数量，当total_pagenum小于allow_pagenum 继续爬
                self.total_pagenum += 1
                yield Request(url=channel_url, meta={'channel_data': channel_url, 'channel': channel_title},
                              callback=self.channel_get)

    def channel_get(self, response):
            anchor_num = response.xpath('//div[@class="gui-main"]/ul/li')
            channel = response.meta['channel']
            for i in anchor_num:
                items = QierItem()  # 实例化item.HuyaItem
                items['channel'] = channel  # 获取频道名称
                str1 = i.xpath('a/div[@class="info-anchor"]/span[@class="popular"]/text()').extract_first()  # 获取观看数量
                pat2 = re.compile(r'[\d+\.\d]*')
                result2 = pat2.findall(str1)
                number = float(result2[0])
                if '万' in str1:
                    number *= 10000
                items['watch_num'] = number
                items['anchor_roomname'] = i.xpath('a/h4[@class="info-livename"]/text()').extract_first()# 获取房间名称
                items['anchor_url'] = 'https://egame.qq.com' + i.xpath('a/@href').extract_first()
                items['anchor_name'] = i.xpath('a/div[@class="info-anchor"]/p[@class="name"]/text()').extract_first()  # 获主播名称
                # print(items['channel'],items['watch_num'],items['anchor_roomname'],items['anchor_name'],items['anchor_url'])
                yield Request(url=items['anchor_url'], meta={'items': items},
                              callback=self.room_parse)
    #
    def room_parse(self, response):
        items = response.meta['items']
        fan_num__ = response.xpath('//span[@class="amount"]/text()').extract_first() # 获取主播订阅数量
        items['fan_num'] = int(str(fan_num__))
        items['crawl_time'] =  self.items_time  # 记录爬取时间
        # items['crawl_time'] = time.strftime('%Y-%m-%d %X', time.localtime())
        yield items  # 输出items