import warnings

# 忽略 scrapy-redis 的警告
warnings.filterwarnings("ignore")

from scrapy.cmdline import execute
execute("scrapy crawl bk".split())
