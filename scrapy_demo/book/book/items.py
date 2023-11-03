# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    authors = scrapy.Field()
    pic = scrapy.Field()
    score = scrapy.Field()