import scrapy,re,json,time
from scrapy.http import Request
from chuso.items import ChusoItem
from runspider import spidertime

class ChusoSpider(scrapy.Spider):
    name = 'chuso'
    allowed_domains = ['www.chushou.tv']  # 设置爬虫允许抓取的
    start_urls = ['http://www.chushou.tv/livezone.htm']  # 设置第一个爬取的url
    allow_pagenum = 5;  # 设置爬取频道的数量
    total_pagenum = 1;  # 计算档前已爬取频道的数量
    url_dict = {}  # 设置存放url的dic
    timetime = spidertime()  # 实例化时间专用类
    items_time = timetime.get_time()  # 记录爬取时间

    def parse(self, response):
        # parse_content = response.xpath('//div[@class="gui-main"]/ul[2]/li')  # 抓取当前频道
        for i in response.xpath('//div[@class="gamezone-areas-con"]/a[@class="zone-item"]'):
            channel_title = i.xpath('div[@class="zone-item-con"]/span[@class="zone-gamename"]/text()').extract()  # 抓取频道名称
            channel_title =channel_title[0]
            # print(channel_title)
            channel_url = 'https://www.chushou.tv' + i.xpath('@href').extract_first()  # 抓取当前频道url
            p = re.compile(r'(?:targetKey=)\d*-*\d*-*\d*')
            tkey = re.findall(r'\d+', "  ".join(re.findall(p, i.xpath('@href').extract_first())))
            tkey = tkey[0] + "-" + tkey[1] + "-" + tkey[2]
            channel_targetKey = tkey
            channel_data = {"url": channel_url, "channel_targetKey":  channel_targetKey}
            if self.total_pagenum <= self.allow_pagenum:  # 用于控制爬出抓取数量，当total_pagenum小于allow_pagenum 继续爬
                self.total_pagenum += 1
                yield Request(url=channel_url, meta={'channel_data': channel_data, 'channel': channel_title},
                              callback=self.channel_get)

    def channel_get(self, response):
        #def parse的回调函数，根据channel_data构造主播数据连接并执行请求
        # page_num = 0
        # page_msg = "?"
        # 抓取当前频道一共有多少页，并转为int格式
        channel_targetKey = response.meta['channel_data']['channel_targetKey']  #用于构造url从而实现翻页
        channel = response.meta['channel']  # 将传入的meta的dict中的channel值赋给channel
        # while page_msg !=
        # for i in range(1, page_num + 1):  # 根据page_num数量构造"下一页"并继续抓取
        url = 'https://www.chushou.tv/nav-list/down.htm?breakpoint={breakpoint}&targetKey={targetKey}'.format(
            breakpoint=0, targetKey=channel_targetKey)
        # 获取下一页的json数据
        yield Request(url=url, meta={'channel': channel, 'channel_targetKey':channel_targetKey},
                        callback=self.channel_parse)  # meta携带数据为频道当前页码，频道名称，回调函数为channel_parse

    def channel_parse(self, response):
        #channel_get 的回调函数，根据返回的json数据抓取相应内容，并抓出主播的房间链接，对房间链接执行请求
        response_json = json.loads(response.text)  # 利用json.loads将json数据转为字典
        channel = response.meta['channel']
        channel_targetKey = response.meta['channel_targetKey']
        # pageitems_msg  = response_json['data']['items']
        page_count = int(response_json['data']['count'])
        # print(channel, page_count, int(page_count/20)+1)
        for i in range(0, int(page_count/20)+1):
            msg_url = 'https://www.chushou.tv/nav-list/down.htm?breakpoint={breakpoint}&targetKey={targetKey}'.format(
                breakpoint=i*20, targetKey=channel_targetKey)
            yield Request(url=msg_url, meta={'channel': channel},
                          callback=self.room_parse)

    def room_parse(self, response):
        response_json = json.loads(response.text)  # 利用json.loads将json数据转为字典
        channel = response.meta['channel']
        for i in response_json['data']['items']:
            items = ChusoItem()  # 实例化item.HuyaItem
            items['channel'] = channel  # 获取频道名称
            items['watch_num'] = i['meta']['subscriberCount']  # 获取观看数量 设置为整数方便排序
            items['anchor_roomname'] = i['name']  # 获取房间名称
            items['anchor_url'] = 'http://www.chushou.tv/room/' + str(i['meta']['roomId']) + '.htm?_fromView=1'
            items['anchor_name'] = i['meta']['creator']  # 获主播名称
            yield Request(url=items['anchor_url'], meta={'items': items},
                          callback=self.room_parse2)

    def room_parse2(self, response):
        items = response.meta['items']
        items['fan_num'] = int(response.xpath('//div[@class="zb_attention_left"]/@data-subscribercount').extract_first())# 获取主播订阅数量
        items['crawl_time'] = self.items_time  # 记录爬取时间
        yield items  # 输出items
