# -*- coding: utf-8 -*-
import os, time

strat_time =  time.strftime('%Y-%m-%d %X', time.localtime())#爬虫统一运行时间
os.system("cd Yy && scrapy crawl yy")#运行爬虫
# os.system("cd Qier && scrapy crawl qier")#运行爬虫
# os.system("cd Chuso && scrapy crawl chuso")#运行爬虫
# os.system("cd Douyu && scrapy crawl douyu")#运行爬虫
# os.system("cd Huya && scrapy crawl huya")#运行爬虫


class spidertime():#该类给爬虫读取时间专用
    times = strat_time
    def get_time(self):
        return self.times

# timetime = spidertime()
# print(timetime.get_time())












# #! /usr/bin/env python3
# # -*- coding: utf-8 -*-
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from scrapy.utils.log import configure_logging
# # 引入spider
# # from Huya.Huya.spiders.huyaspider import HuyaspiderSpider
# from Yy.Yy.spiders.Yyspider import YyspiderSpider
# # from Qier.qier.spiders.qierspider import qierSpider
# import logging, time
#
#
#
# logger = logging.getLogger(__name__)
#
# settings = get_project_settings()
# configure_logging(settings)
# runner = CrawlerRunner(settings)
# # Runtime = time.strftime('%Y-%m-%d %X', time.localtime())  # 记录爬取时间
#
# # def Runtime():
# #     return Runtime
#
# def start_spider():
#     # 装载爬虫
#     # runner.crawl(HuyaspiderSpider)
#
#     runner.crawl(YyspiderSpider)
#     # runner.crawl(qierSpider)
#
#     # 爬虫结束后停止事件循环
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#
#     # 启动事件循环
#     reactor.run()
#
#
# def main():
#     start_spider()
#
# if __name__ == '__main__':
#     main()
