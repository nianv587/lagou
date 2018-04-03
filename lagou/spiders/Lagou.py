# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lagou.items import LagouJobItemLoader, LagouJobItem
from datetime import datetime


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    # custom_settings = {
    #     # "COOKIES_ENABLED": False,
    #     # "DOWNLOAD_DELAY": 1,
    #     'DEFAULT_REQUEST_HEADERS': {
    #         'Accept': 'application/json, text/javascript, */*; q=0.01',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         # 'Accept-Language': 'zh-CN,zh;q=0.8',
    #         # 'Connection': 'keep-alive',
    #         'Cookie':'user_trace_token=20171015132411-12af3b52-3a51-466f-bfae-a98fc96b4f90; LGUID=20171015132412-13eaf40f-b169-11e7-960b-525400f775ce; SEARCH_ID=070e82cdbbc04cc8b97710c2c0159ce1; ab_test_random_num=0; X_HTTP_TOKEN=d1cf855aacf760c3965ee017e0d3eb96; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsXIrWUxpNGLE2g_bKzlUCXPTRJMHxfCs6L20RqgCpUq%26wd%3D%26eqid%3Dee53adaf00026e940000000559e354cc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotjob; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG50060B788C4EED616EB9D1BF30380575; _gat=1; _ga=GA1.2.471681568.1508045060; LGSID=20171015203008-94e1afa5-b1a4-11e7-9788-525400f775ce; LGRID=20171015204552-c792b887-b1a6-11e7-9788-525400f775ce',
    #         # 'Host': 'www.lagou.com',
    #         # 'Origin': 'https://www.lagou.com',
    #         # 'Referer': 'https://www.lagou.com/',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    #     }
    # }

    rules = (
        Rule(LinkExtractor(allow=("zhaoping/.*")), follow=True),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html*",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )


    def parse_job(self, response):
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_xpath("title", "//*[@class='job-name']/@title")
        item_loader.add_xpath("salary", "//*[@class='job_request']/p/span[@class='salary']/text()")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")
        item_loader.add_xpath("tags", "//*[@class='position-label clearfix']/li/text()")
        item_loader.add_xpath("publish_time", "//*[@class='publish_time']/text()")
        item_loader.add_xpath("job_advantage", "//*[@class='job-advantage']/p/text()")
        item_loader.add_xpath("job_desc", "string(//*[@class='job_bt']/div)")
        item_loader.add_xpath("job_addr", "//*[@class='work_addr']")
        item_loader.add_xpath("company_name", "//*[@class='job_company']/dt/a/img/@alt")
        item_loader.add_xpath("company_url", "//*[@class='job_company']/dt/a/@href")
        item_loader.add_value("url", response.url)
        item_loader.add_value("crawl_time", datetime.now())
        job_item = item_loader.load_item()

        yield job_item

