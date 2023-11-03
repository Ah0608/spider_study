# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyRedisdemo1Item(scrapy.Item):
    # define the fields for your item here like:
    # title = scrapy.Field()
    # type = scrapy.Field()
    # pub_time = scrapy.Field()
    # score = scrapy.Field()
    # context = scrapy.Field()

    name = scrapy.Field()
    price = scrapy.Field()
    author = scrapy.Field()
    pub_time = scrapy.Field()
    Publisher = scrapy.Field()
    introduction = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
