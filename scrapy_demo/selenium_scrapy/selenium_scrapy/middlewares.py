# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
class SeleniumMiddleware(object):

    def process_request(self, request, spider):
        chrome_options = Options()
        # 启用无头模式
        chrome_options.add_argument("--headless")
        url = request.url
        browser = webdriver.Chrome(options=chrome_options,executable_path=r'C:\Users\Administrator\PycharmProjects\spider_study\scrapy_demo\selenium_scrapy\selenium_scrapy\spiders\chromedriver.exe')
        browser.get(url)
        time.sleep(5)
        html = browser.page_source
        browser.close()
        return HtmlResponse(url=request.url,
                            body=html,
                            request=request,
                            encoding='utf-8',
                            status=200)
