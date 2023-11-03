# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from curl_cffi import requests
from scrapy.http import HtmlResponse

from scrapy_demo.scrapy_redisDemo1.scrapy_redisDemo1.settings import ProxyPool

# from scrapy import signals
#
# # useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter
#
#
# class ScrapyRedisdemo1SpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request or item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)
#
#
# class ScrapyRedisdemo1DownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)

proxypool = ProxyPool()
from fake_useragent import UserAgent

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": UserAgent().random,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "http://search.dangdang.com/?key=%CA%E9&act=input",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
cookies = {
    "MDD_channelId": "70000",
    "MDD_fromPlatform": "307",
    "__permanent_id": "20230915103120922170542399530493725",
    "ddscreen": "2",
    "__visit_id": "20231025111644039536828686236742697",
    "__out_refer": "",
    "dest_area": "country_id%3D9000%26province_id%3D111%26city_id%3D0%26district_id%3D0%26town_id%3D0",
    "__rpm": "mix_317715...1698203813359%7Cs_112100.155956512835%2C155956512836..1698203865012",
    "search_passback": "92c6082a70776842d8883865fc0100003dff6400ce883865",
    "__trace_id": "20231025111746107200407128141313147",
    "pos_9_end": "1698203866673",
    "pos_0_start": "1698203866690",
    "pos_0_end": "1698203866705",
    "ad_ids": "3643545%2C3608930%2C3618803%7C%232%2C2%2C1"
}

class RandomHeadersProxyMiddleware:

    def process_request(self, request, spider):
        ip = proxypool.get_random_proxy()
        proxy = {"http": "http://{}".format(ip), "https": "http://{}".format(ip)}
        try:
            response = requests.get(request.url, headers=headers, cookies=cookies, impersonate='chrome110', proxies=proxy)
            html = response.content.decode("gb2312", errors='replace')
            return HtmlResponse(url=request.url,
                                body=html,
                                request=request,
                                encoding='utf-8',
                                status=200)
        except Exception as e:
            if 'Received HTTP code 454 from proxy after CONNECT' in str(e):
                proxypool.delete_proxy(ip)
                print(ip, '已删除')

