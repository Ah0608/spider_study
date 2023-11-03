# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time

from pyppeteer import launch
from scrapy.http import HtmlResponse
import asyncio
import logging
from twisted.internet.defer import Deferred #不使用gerapy_pyppeteer时打开，使用则注释

from .settings import ips, ua_pool

# logging.getLogger('websockets').setLevel('INFO')
# logging.getLogger('pyppeteer').setLevel('INFO')
#
#
# def as_deferred(f): #不使用gerapy_pyppeteer时打开，使用则注释
#     return Deferred.fromFuture(asyncio.ensure_future(f))
#
#
# class PyppeteerMiddleware(object):
#
#     async def _process_request(self, request, spider):
#         proxy_server = random.choice(ips)
#         browser = await launch(headless=False,args=[f'--proxy-server={proxy_server}'])
#         page = await browser.newPage()
#         await page.setExtraHTTPHeaders({
#             'User-Agent': random.choice(ua_pool)
#         })
#         pyppeteer_response = await page.goto(request.url)
#         await asyncio.sleep(3)
#         prev_element_count = 0  # 上一次的元素数量
#         consecutive_no_increase_count = 0  # 连续未增加的次数
#         while consecutive_no_increase_count < 3:
#             # 滚动到页面底部
#             await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             # 等待页面加载完整
#             time.sleep(1)
#             await page.waitForSelector("li.car-list_item__3nyEK")
#             # 统计当前元素数量
#             ele = await page.querySelectorAll("li.car-list_item__3nyEK")
#             current_element_count = len(ele)
#             if current_element_count > prev_element_count:
#                 consecutive_no_increase_count = 0
#             else:
#                 consecutive_no_increase_count += 1
#             prev_element_count = current_element_count
#
#         html = await page.content()
#         pyppeteer_response.headers.pop('content-encoding', None)
#         pyppeteer_response.headers.pop('Content-Encoding', None)
#         response = HtmlResponse(
#             page.url,
#             status=pyppeteer_response.status,
#             headers=pyppeteer_response.headers,
#             body=str.encode(html),
#             encoding='utf-8',
#             request=request
#         )
#         await page.close()
#         await browser.close()
#         return response
#
#     def process_request(self, request, spider):
#         return as_deferred(self._process_request(request, spider))


import random

class RandomHeadersProxyMiddleware:

    def process_request(self, request, spider):
        # 随机选择 User-Agent
        request.headers['User-Agent'] = random.choice(ua_pool)

        # 随机选择代理 IP
        proxy = random.choice(ips)
        request.meta['proxy'] = proxy