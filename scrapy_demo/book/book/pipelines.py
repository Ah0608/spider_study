# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from sqlalchemy import create_engine
from scrapy.pipelines.images import ImagesPipeline
mysql_5_book = create_engine("mysql+pymysql://root:root@localhost:3306/demo2",pool_recycle=3600)
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
def read_sql(db_engine, sql, value_data=()):#value_data可不填
    with db_engine.connect() as conn:
        result = conn.execute(sql, value_data)
        result_list = result.fetchall()#返回多个元组/记录
    return result_list#返回的是元组


def write_sql(db_engine,sql, value_data=()):#value_data:插入值的类型是元组
    with db_engine.connect() as conn:
        conn.execute(sql, value_data)


#保存数据
def save_data(dict,table_name,mysql_engine):
    keys = ','.join(dict.keys())
    values = ','.join(['%s'] * len(dict.keys()))
    sql = """INSERT INTO {table_name} ({keys}) values ({values});""".format(table_name=table_name,keys=keys, values=values)
    # print(sql)
    val = tuple(dict.values())
    try:
        write_sql(mysql_engine, sql, val)
        # print("插入数据成功！")
        print('save_ok')
    except Exception as e:
        print(e)
        pass

class BookPipeline:
    def process_item(self, item, spider):
       item = dict(item)
       save_data(item,'book_list',mysql_5_book)


class picPipeline(ImagesPipeline):
    # 重写 get_media_requests()方法，将图片的链接交给调度器入队列即可
    def get_media_requests(self, item, info): # 传入图片url和图片名称
        yield scrapy.Request(url=item["pic"], meta={"title": item['name']})

    # 重写file_path()方法 处理文件路径及文件名
    def file_path(self, request, response=None, info=None, *, item=None):
        image_title = request.meta['title']
        filename = image_title + '.jpg'  # 拼接图片名称
        return filename






