# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlspiderdemoItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    categories = scrapy.Field()
    pub_time = scrapy.Field()
    Score = scrapy.Field()

