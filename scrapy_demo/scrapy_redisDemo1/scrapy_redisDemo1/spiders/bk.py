import parsel
import scrapy
from scrapy.http import HtmlResponse
from scrapy_redis.spiders import RedisSpider

from ..items import ScrapyRedisdemo1Item


class BkSpider(RedisSpider):
    name = "bk"
    # allowed_domains = ["category.dangdang.com"]
    # start_urls = ["http://category.dangdang.com/"]
    # redis_key = 'bk:start_urls'
    index = 1

    def start_requests(self):
        for page in range(1,10):
            url = 'http://search.dangdang.com/?key=%CA%E9&act=input&page_index={}'.format(page)
            print(url)
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True, )

    def parse(self, response:HtmlResponse):
        item = ScrapyRedisdemo1Item()
        sel = parsel.Selector(response.text)
        lis = sel.xpath("//ul[@class='bigimg']/li")
        for li in lis:
            item['name'] = li.xpath(".//p[@class='name']/a/@title").get(default='').strip()
            item['price'] = li.xpath(".//p[@class='price']/span/text()").get(default='').strip()
            item['author'] = ''.join(li.xpath(".//p[@class='search_book_author']/span[1]//text()").getall())
            item['pub_time'] = li.xpath(".//p[@class='search_book_author']/span[2]/text()").get(default='').strip().replace('/','')
            item['Publisher'] = li.xpath(".//p[@class='search_book_author']/span[3]/a/text()").get(default='').strip()
            item['introduction'] = li.xpath(".//p[@class='detail']/text()").get(default='').replace(' ','').replace('\n','')
            item['url'] = 'http:' + li.xpath(".//p[@class='name']/a/@href").get(default='')
            item['image_url'] = 'http:' + li.xpath(".//img/@data-original").get(default='')
            yield item
            print(item)
        # next = response.urljoin(sel.xpath("//li[@class='next']/a/@href").get(default=''))
        # if self.index < 10:
        #     self.index = self.index + 1
        #     next_url = 'http://search.dangdang.com/?key=%CA%E9&act=input&page_index={}'.format(self.index)
        #     print('正在请求：',next_url)
        #     yield scrapy.Request(url=next_url,callback=self.parse,dont_filter=True)

