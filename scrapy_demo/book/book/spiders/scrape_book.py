import scrapy
from scrapy import Request
from ..items import BookItem


class ScrapeBookSpider(scrapy.Spider):
    name = "scrape_book"
    # allowed_domains = ["antispider3.scrape.center"]
    # start_urls = ["https://spa5.scrape.center/api/book/?limit=18&offset=0"]
    def start_requests(self):
        urls = [f'https://spa5.scrape.center/api/book/?limit=18&offset={i}' for i in range(0, 37, 18)]
        for url in urls:
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        # print(response.WebRequest.headers['User-Agent'])
        # print(response.WebRequest.headers.getlist('Cookie'))
        # print(response.WebRequest.meta['proxy'])
        print('--------------输出内容：')
        json_data = response.json()
        results = json_data['results']

        item = BookItem()
        for result in results:
            item['id'] = result['id'].strip()
            item['name'] = result['name'].strip()
            au = result['authors']
            item['authors'] = ''.join(au).replace('\n', '').replace(' ', '').strip()
            item['pic'] = result['cover'].strip()
            item['score'] = result['score'].strip()
            yield item
            # print(item)

