# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DcdItem(scrapy.Item):
    car_name = scrapy.Field()
    car_id = scrapy.Field()
    car_price = scrapy.Field()
    car_score = scrapy.Field()
    detail_url = scrapy.Field()
    image_url = scrapy.Field()
    brand_name = scrapy.Field()
    brand_id = scrapy.Field()
    business_status = scrapy.Field()

