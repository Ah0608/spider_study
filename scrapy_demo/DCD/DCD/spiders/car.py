import json
import random
import time

import parsel
import scrapy
from gerapy_pyppeteer import PyppeteerRequest
from scrapy import Request, FormRequest

from ..items import DcdItem
from ..settings import read_sql, mysql_engine, write_sql


class CarSpider(scrapy.Spider):
    name = "car"
    # allowed_domains = ["https://www.dongchedi.com"]

    def start_requests(self):
        sql = "SELECT id,brand_id,brand_name,brand_url FROM brand_list WHERE download_state is Null"
        data = read_sql(mysql_engine,sql)
        for i in data:
            id,brand_id, brand_name, brand_url = i
            for j in range(1,6):
                print('正在请求{}的第{}页数据...'.format(brand_name,j))
                time.sleep(random.randint(1,3))
                if j == 1:
                    yield Request(url=brand_url,callback=self.get_parse,meta={'id':id})
                else:
                    POST_URL = 'https://www.dongchedi.com/motor/pc/car/brand/select_series_v2?aid=1839&app_name=auto_web_pc'
                    data = {
                        'brand': str(brand_id),
                        'sort_new': 'hot_desc',
                        'city_name': '重庆',
                        'limit': '30',
                        'page': str(j),
                    }
                    yield FormRequest(url=POST_URL,callback=self.post_parse,formdata=data)
            print('{}请求结束...'.format(brand_name))
            sql_update = 'update brand_list set download_state=%s where id=%s;'
            write_sql(mysql_engine, sql_update, ('已采集', id))
    def get_parse(self, response):
        print('正在使用的代理：',response.request.meta['proxy'])
        sel = parsel.Selector(response.text)
        js = sel.xpath('//*[@id="__NEXT_DATA__"]/text()').get(default='')
        json_data = json.loads(js)
        item = DcdItem()
        for i in json_data['props']['pageProps']['seriesInfo']['series']:
            item['car_name'] = i['outter_name']
            item['car_score'] = i['dcar_score']
            item['detail_url'] = 'https://www.dongchedi.com/auto/series/score/{}-x-x-x-x-x-x'.format(i['concern_id'])
            item['car_id'] = i['concern_id']
            item['car_price'] = i['official_price']
            item['image_url'] = i['cover_url']
            item['brand_name'] = i['brand_name']
            item['brand_id'] = i['brand_id']
            item['business_status'] = i['business_status']
            yield item
    def post_parse(self, response):
        print('正在使用的代理：', response.request.meta['proxy'])
        if response.status != 200:
            print('该页没有数据!')
            return
        json_data = response.json()
        item = DcdItem()
        for i in json_data['data']['series']:
            item['car_name'] = i['outter_name']
            item['car_score'] = i['dcar_score']
            item['detail_url'] = 'https://www.dongchedi.com/auto/series/score/{}-x-x-x-x-x-x'.format(i['concern_id'])
            item['car_id'] = i['concern_id']
            item['car_price'] = i['official_price']
            item['image_url'] = i['cover_url']
            item['brand_name'] = i['brand_name']
            item['brand_id'] = i['brand_id']
            item['business_status'] = i['business_status']
            yield  item
