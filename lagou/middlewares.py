# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import redis
import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from lagou.lagoulogin import init_lagou_cookie

class LagouCookiesMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        self.rconn = redis.from_url(settings['REDIS_URL'], db=5, decode_responses=True)
        init_lagou_cookie(self.rconn, crawler.spider.name)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        redisKeys = self.rconn.keys()
        if len(redisKeys) > 0:
            elem = random.choice(redisKeys)
            if spider.name + ':Cookies' in elem:
                cookie = eval(self.rconn.get(elem))
                request.cookies = cookie
                request.meta["accountText"] = elem.split("Cookies:")[-1]