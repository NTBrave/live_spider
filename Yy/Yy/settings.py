# -*- coding: utf-8 -*-


BOT_NAME = 'Yy'

SPIDER_MODULES = ['Yy.spiders']
NEWSPIDER_MODULE = 'Yy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Yy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'Yy.pipelines.YyPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    'Yy.middlewares.YyUserAgentMiddleware': 400,                      #启动middlewares中设定好的usragent
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':None,   #禁用默认的usragent
}
