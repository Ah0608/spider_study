import json

import scrapy
from scrapy import Request


class Movie01Spider(scrapy.Spider):
    name = "movie01"
    # allowed_domains = ["antispider7.scrape.center"]
    # start_urls = ["http://antispider7.scrape.center/"]
    def start_requests(self):
        urls = ['https://antispider7.scrape.center/api/book/?limit=18&offset={}'.format(_) for _ in range(0,1,18)]
        for url in urls:
            yield Request(url=url,callback=self.parse)

    def parse(self, response):
        print(response)
        text = response.text
        JSON_DATA = json.loads(text)
        print(JSON_DATA)
