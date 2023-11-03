import scrapy
from gerapy_pyppeteer import PyppeteerRequest
from scrapy import Request


class Book02Spider(scrapy.Spider):
    name = "book02"
    def parse(self, response):
        print('--------------输出内容：')
        divs = response.xpath('//div[@class="el-col el-col-4"]')
        for div in divs:
            art_url = div.xpath('.//div[@class="top el-row"]//a/@href').get(default='')
            print(art_url)

    def start_requests(self):
        urls = [f'https://spa5.scrape.center/page/{i}' for i in range(1, 7)]
        for url in urls:
            print(url)
            yield PyppeteerRequest(url=url, callback=self.parse)