from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader #
from itemloaders.processors import TakeFirst,Identity,Compose #
from scrapy.spiders import CrawlSpider, Rule
from ..items import CrawlspiderdemoItem

# 定义ItemLoader的子类名为MovieItemLoader
class MovieItemLoader(ItemLoader):
    default_output_processor = TakeFirst() #默认情况下，每一个字段取第一个值相当于调用了extract_first()
    categories_out = Identity() # categories字段默认保持不变
    Score_out = Compose(TakeFirst(),str.strip) #Score字段去除前后空格


class MovieSpider(CrawlSpider):
    name = "movie"
    allowed_domains = ["ssr1.scrape.center"]
    start_urls = ["http://ssr1.scrape.center/"]
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='el-card item m-t is-hover-shadow']//a[@class='name']"), callback="parse_item", follow=True),
        # Rule(LinkExtractor(restrict_css=".next"), follow=True)
        )
    def parse_item(self, response):
        print(response.url)
        loader = MovieItemLoader(item=CrawlspiderdemoItem(),response=response)
        loader.add_xpath('Title',"//h2[@class='m-b-sm']//text()")
        loader.add_xpath('categories',"//div[@class='categories']/button/span/text()")
        loader.add_xpath('pub_time',"//div[@class='m-v-sm info']/span[contains(text(),'上映')]/text()")
        loader.add_xpath('Score',"//p[@class='score m-t-md m-b-n-sm']/text()")
        yield loader.load_item()
