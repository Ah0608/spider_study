import parsel
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider

from ..items import ScrapyRedisdemo1Item


class MvSpider(RedisCrawlSpider):
    name = "mv"
    # allowed_domains = ["ssr1.scrape.center"]
    # start_urls = ["http://ssr1.scrape.center/"]
    redis_key = 'mv:start_urls'

    rules = (
        Rule(LinkExtractor(restrict_css=".name"),
             callback="parse_item", follow=False),
        Rule(LinkExtractor(restrict_css=".number a"), follow=True)
    )

    def parse_item(self, response):
        item = ScrapyRedisdemo1Item()
        sel = parsel.Selector(response.text)
        item['title'] = sel.xpath("//h2[@class='m-b-sm']/text()").get(default='').strip()
        item['type'] = '/'.join(sel.xpath("//div[@class='categories']//span/text()").getall())
        item['pub_time'] = sel.xpath("//div[@class='m-v-sm info']/span[contains(text(),'上映')]/text()").get(default='').replace('上映','')
        item['score'] = sel.xpath("//p[@class='score m-t-md m-b-n-sm']/text()").get(default='').replace(' ','').replace('\n','')
        item['context'] = sel.xpath("//div[@class='drama']/p/text()").get(default='').replace(' ','').replace('\n','')
        yield item
