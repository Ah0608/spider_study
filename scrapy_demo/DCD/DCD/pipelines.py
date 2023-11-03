# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .settings import mysql_engine, save_data


class DcdPipeline:
    # def open_spider(self,spider):
    #     mysql_engine


    def process_item(self, item, spider):
        save_data(item,'car_list',mysql_engine)

