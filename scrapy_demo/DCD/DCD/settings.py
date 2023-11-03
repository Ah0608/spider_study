# Scrapy settings for DCD project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from sqlalchemy import create_engine

BOT_NAME = "DCD"

SPIDER_MODULES = ["DCD.spiders"]
NEWSPIDER_MODULE = "DCD.spiders"

# mysql引擎
mysql_engine = create_engine("mysql+pymysql://root:root@localhost:3306/demo2",pool_recycle=3600)

# ip池
ips = ['http://192.168.1.171:8118',
       'http://192.168.1.183:38118',
       'http://111.177.63.86:8888',
       'http://106.11.226.232:8009',
       'http://117.71.112.190:8888',
       'http://139.224.67.166:7890',
       ]

# ua池
ua_pool = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',]

# 日志等级
LOG_LEVEL = 'ERROR'

# 设置请求间隔时间
DOWNLOAD_DELAY = 3

DOWNLOAD_TIMEOUT = 10

# GERAPY_PYPPETEER配置参数
CONCURRENT_REQUESTS = 2 # 请求并发数量
GERAPY_PYPPETEER_HEADLESS = True # 是否开启浏览器无头模式
GERAPY_PYPPETEER_PRETEND = True # 开启webdriver反屏蔽功能

# 读sql
def read_sql(db_engine, sql, value_data=()):
    with db_engine.connect() as conn:
        result = conn.execute(sql, value_data)
        result_list = result.fetchall()
    return result_list


def write_sql(db_engine,sql, value_data=()):#value_data:插入值的类型是元组
    with db_engine.connect() as conn:
        conn.execute(sql, value_data)

def save_data(dict,table_name,mysql_engine):
    keys = ','.join(dict.keys())
    values = ','.join(['%s'] * len(dict.keys()))
    sql = """INSERT INTO {table_name} ({keys}) values ({values});""".format(table_name=table_name,keys=keys, values=values)
    # print(sql)
    val = tuple(dict.values())
    try:
        write_sql(mysql_engine, sql, val)
        print('save_ok')
    except Exception as e:
        print(e)
        pass

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "DCD (+http://www.yourdomain.com)"

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
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
#    "DCD.middlewares.DcdSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "DCD.middlewares.DcdDownloaderMiddleware": 543,
   # "DCD.middlewares.PyppeteerMiddleware": 543,
   "DCD.middlewares.RandomHeadersProxyMiddleware": 543,
   # 'gerapy_pyppeteer.downloadermiddlewares.PyppeteerMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "DCD.pipelines.DcdPipeline": 300,
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
