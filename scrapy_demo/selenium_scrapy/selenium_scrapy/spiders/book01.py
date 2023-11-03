import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse
from gerapy_selenium import SeleniumRequest

class Book01Spider(scrapy.Spider):
    name = "book01"
    def parse(self, response:HtmlResponse):
        print('--------------输出内容：')
        divs = response.xpath('//div[@class="el-col el-col-4"]')
        for div in divs:
            art_url = div.xpath('.//div[@class="top el-row"]//a/@href').get(default='')
            print(art_url)

    def start_requests(self):
        urls = [f'https://spa5.scrape.center/page/{i}' for i in range(1,9)]
        for url in urls:
            print(url)
            yield SeleniumRequest(url=url, callback=self.parse)