import logging
from datetime import datetime

from scrapy import signals

logging.basicConfig(
    filemode = 'a',         # 文件模式
    format = '%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',  # 时间格式 format中asctime
    level=logging.INFO  # 日志级别
)


class TimingExtension:
    def __init__(self):
        self.start_time = None
        self.finish_time = None
        self.item_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.request_scheduled, signal=signals.request_scheduled)

        return ext

    def item_scraped(self, item, spider):
        self.item_count += 1

    def spider_opened(self, spider):
        self.start_time = datetime.now()

    def spider_closed(self, spider):
        self.finish_time = datetime.now()
        self.log_timing_information(spider)
        self.log_item_count(spider)

    def request_scheduled(self, request, spider):
        self.log_request_url(request,spider)

    def log_request_url(self, request,spider):
        url = request.url
        logging.info(f'{spider.name}正在请求的url是: {url}')

    def log_timing_information(self,spider):
        if self.start_time and self.finish_time:
            start_time_str = self.start_time.strftime('%Y-%m-%d %H:%M:%S')
            finish_time_str = self.finish_time.strftime('%Y-%m-%d %H:%M:%S')
            duration = self.finish_time - self.start_time
            logging.info(f"{spider.name}爬取开始时间：{start_time_str}")
            logging.info(f"{spider.name}爬取结束时间：{finish_time_str}")
            logging.info(f"{spider.name}爬取总耗时：{duration}")

    def log_item_count(self,spider):
        logging.info(f"{spider.name}爬取的Item总数：{self.item_count}")
        logging.info('-'*60+f'{self.finish_time}'+'-'*60)
