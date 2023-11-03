# Scrapy settings for scrapy_redisDemo1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scrapy_redisDemo1"

SPIDER_MODULES = ["scrapy_redisDemo1.spiders"]
NEWSPIDER_MODULE = "scrapy_redisDemo1.spiders"


# 1.启用调度将请求存储进redis  必须
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 2.确保所有spider通过redis共享相同的重复过滤。  必须
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 3.可选 # 不清理redis队列，允许暂停/恢复抓取。
# 允许暂定,redis数据不丢失
SCHEDULER_PERSIST = False
# 4.指定连接到Redis时要使用的主机和端口。  必须
REDIS_HOST = '192.168.1.186'
REDIS_PORT = 6379
REDIS_DB = '1'
LOG_LEVEL = 'INFO'
# 设置超时时间
DOWNLOAD_TIMEOUT = 10
# 设置重新请求次数
RETRY_TIMES = 5
# 出现这些状态码会重复进行请求
# HTTPERROR_ALLOWED_CODES = [404, 403, 301, 500, 407]
# 是否开启 retry功能
RETRY_ENABLED = True


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "scrapy_redisDemo1 (+http://www.yourdomain.com)"

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 20
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "scrapy_redisDemo1.middlewares.ScrapyRedisdemo1SpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "scrapy_redisDemo1.middlewares.RandomHeadersProxyMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # "scrapy_redisDemo1.pipelines.ScrapyRedisdemo1Pipeline": 300,
    'scrapy_redis.pipelines.RedisPipeline':300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# REDIS
import logging
import random
import redis


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class ProxyPool():
    def __init__(self, host='192.168.1.186', port=6379,db=2):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def add_proxy(self, ip, score=100):
        self.redis.zadd('proxies', {ip: score})
        logging.info(f'{ip} save_ok!')

    def decrease_score(self, ip):
        current_score = self.redis.zscore('proxies', ip)
        if current_score is not None:
            new_score = max(current_score - 1, 0)
            self.redis.zadd('proxies', {ip: new_score})
            if new_score == 0:
                self.delete_proxy(ip)

    def delete_proxy(self, ip):
        self.redis.zrem('proxies', ip)

    def get_random_proxy(self):
        set_key = 'proxies'
        members = self.redis.zrange(set_key, 0, -1)
        random_member = random.choice(members)
        return random_member.decode()

    def get_proxy_list(self):
        set_key = 'proxies'
        ip_list = self.redis.zrange(set_key, 0, -1)
        proxty_list = [i.decode() for i in ip_list]
        return proxty_list

    def check_proxy(self):
        set_key = 'proxies'
        ips = self.redis.zrange(set_key, 0, -1)
        return ips



