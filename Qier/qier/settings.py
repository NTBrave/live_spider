# -*- coding: utf-8 -*-
BOT_NAME = 'qier'

SPIDER_MODULES = ['qier.spiders']
NEWSPIDER_MODULE = 'qier.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qier (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES = [400]
ITEM_PIPELINES = {
   'qier.pipelines.QierPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
   'qier.middlewares.QierUserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':None,   #禁用默认的usragent
}
