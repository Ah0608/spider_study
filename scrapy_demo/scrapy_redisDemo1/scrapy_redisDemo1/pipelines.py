# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from redis import StrictRedis
from sqlalchemy import create_engine

from 工具.tool import save_data

rediscli = StrictRedis(host='192.168.1.186', port=6379, db=1, decode_responses=True)
mysql_engine = create_engine("mysql+pymysql://root:root@localhost:3306/demo2", pool_recycle=3600)

class ScrapyRedisdemo1Pipeline:
    pass
    # def process_item(self, item, spider):
    #     while True:
    #         source, data = rediscli.blpop(["mv:items"])
    #         item = json.loads(data)
    #         print(item)
    #         save_data(item, 'movie_list', mysql_engine)

