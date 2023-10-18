import logging
from concurrent.futures import ThreadPoolExecutor
from sys import stdout

import requests

from my_crawl.ip_pool.Redis_ip import ProxyPool
from my_crawl.tool.utils import get_ua

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=stdout)


def fetch_url(ip):
    ip = ip.decode()
    logging.info(f'{ip} --正在检测中请稍等...')
    proxy = {"http": f"http://{ip}", "https": f"http://{ip}"}
    REQUEST_URL = 'https://www.baidu.com'
    IP_RATING = 100
    retry_count = 0
    max_retries = 20  # 最大请求次数
    while retry_count < max_retries:
        try:
            response = requests.get(REQUEST_URL, proxies=proxy, headers=get_ua(), timeout=5)
            response.raise_for_status()  # 如果返回的状态码不是200，会抛出异常
        except requests.exceptions.RequestException:
            IP_RATING = IP_RATING - 5
        retry_count = retry_count + 1
    print(f'{ip} --的评分是:{IP_RATING}')
    if IP_RATING < 80:
        proxy_pool = ProxyPool()
        proxy_pool.delete_proxy(ip)
        logging.info(f'该{ip} --已成功删除')


def multi_thread_check_ip_by_baidu():
    proxy_pool = ProxyPool()
    ips = proxy_pool.check_proxy()
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(fetch_url, ips)


if __name__ == '__main__':
    multi_thread_check_ip_by_baidu()

