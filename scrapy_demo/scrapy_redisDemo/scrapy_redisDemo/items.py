# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyRedisdemoItem(scrapy.Item):
    # define the fields for your item here like:
    film_name = scrapy.Field()
    score = scrapy.Field()
    director = scrapy.Field()
    detail = scrapy.Field()

