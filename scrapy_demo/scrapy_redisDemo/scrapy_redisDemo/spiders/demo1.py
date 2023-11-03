import scrapy
from scrapy_redis.spiders import RedisSpider

class Demo1Spider(RedisSpider):
    name = "demo1"
    # allowed_domains = ["dongchedi.com"]
    # start_urls = ["http://dongchedi.com/"]
    redis_key = 'db:start_urls'  # 开启爬虫钥匙

    def parse(self, response):
        filename = 'image' + '/' + response.url.split('~tplv')[0].split('/')[-1] + '.png'
        print(filename)
        with open(filename, 'wb') as f:
            f.write(response.body)

