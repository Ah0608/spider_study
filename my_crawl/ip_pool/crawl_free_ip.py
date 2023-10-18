import base64
import json
import logging
import random
import re
import subprocess
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from sys import stdout

import parsel
import requests
from playwright.sync_api import sync_playwright

from my_crawl.WebRequest.RequestHttp import get_request
from my_crawl.ip_pool.Redis_ip import ProxyPool
from my_crawl.tool.utils import get_ua, request_proxy

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=stdout)

proxypool = ProxyPool()


def checking_ip(ip):
    print(f'IP：{ip} 检测为：')
    proxy = {"http": f"http://{ip}", "https": f"http://{ip}"}
    url = 'https://www.baidu.com/'
    try:
        response = requests.get(url, proxies=proxy, timeout=10)
        response.raise_for_status()  # 检查响应状态码是否为 200
        print('yes')
        proxypool.add_proxy(ip)
    except requests.exceptions.RequestException:
        print('no')


def multi_thread_check(ips):
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(checking_ip, ips)


def get_zdy():  # 站大爷
    urls = [f'https://www.zdaye.com/free/{PAGE}/?dengji=3' for PAGE in range(1, 5)]
    IPS = []
    for url in urls:
        try:
            logging.info(f'正在获取 {url} 的IP')
            selector = parsel.Selector(get_request(url, headers=get_ua(), verify=False, proxy=request_proxy).text)
        except:
            multi_thread_check(IPS)
            return
        ip_info = selector.xpath('//table[@id="ipc"]//tbody/tr')
        for i in ip_info:
            ipaddress = i.xpath('./td[1]/text()').get(default='')
            port = i.xpath('./td[2]/text()').get(default='')
            IP = f'{ipaddress}:{port}'
            IPS.append(IP)
        time.sleep(10)
    multi_thread_check(IPS)


def get_kdl():  # 快代理
    urls = [f'https://www.kuaidaili.com/free/inha/{PAGE}/' for PAGE in range(1, 6)]
    urls.extend([f'https://www.kuaidaili.com/free/intr/{PAGE}/' for PAGE in range(1, 6)])
    IPS = []
    for url in urls:
        try:
            logging.info(f'正在获取 {url} 的IP')
            selector = parsel.Selector(get_request(url, headers=get_ua(), verify=False, proxy=request_proxy).text)
        except:
            multi_thread_check(IPS)
            return
        ip_info = selector.xpath('//tbody/tr')
        for i in ip_info:
            ipaddress = i.xpath('./td[@data-title="IP"]/text()').get(default='').strip()
            port = i.xpath('./td[@data-title="PORT"]/text()').get(default='').strip()
            IP = f'{ipaddress}:{port}'
            IPS.append(IP)
        time.sleep(5)
    multi_thread_check(IPS)


def get_ydl():  # 云代理
    urls = [f'http://www.ip3366.net/free/?stype=1&page={PAGE}' for PAGE in range(1, 6)]
    urls.extend([f'http://www.ip3366.net/free/?stype=2&page={PAGE}' for PAGE in range(1, 6)])
    IPS = []
    for url in urls:
        try:
            logging.info(f'正在获取 {url} 的IP')
            selector = parsel.Selector(get_request(url, headers=get_ua(), verify=False, proxy=request_proxy).text)
        except:
            multi_thread_check(IPS)
            return
        ip_info = selector.xpath('//tbody/tr')
        for i in ip_info:
            ipaddress = i.xpath('./td[1]/text()').get(default='').strip()
            port = i.xpath('./td[2]/text()').get(default='').strip()
            IP = f'{ipaddress}:{port}'
            IPS.append(IP)
        time.sleep(5)
    multi_thread_check(IPS)


def get_66():  # 66代理
    url = 'http://www.66ip.cn/nmtq.php?getnum=100&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip'
    IPS = []
    try:
        logging.info(f'正在获取 {url} 的IP')
        text = get_request(url, headers=get_ua(), verify=False, proxy=request_proxy).text
    except:
        multi_thread_check(IPS)
        return
    pattern = r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)\b"
    ips = re.findall(pattern, text)
    print(ips)
    multi_thread_check(ips)


def get_kaix():  # 开心代理
    urls = [f'http://www.kxdaili.com/dailiip/1/{PAGE}.html' for PAGE in range(1, 6)]  # 高匿
    urls.extend([f'http://www.kxdaili.com/dailiip/2/{PAGE}.html' for PAGE in range(1, 6)])
    IPS = []
    for url in urls:
        try:
            logging.info(f'正在获取 {url} 的IP')
            selector = parsel.Selector(get_request(url, headers=get_ua(), proxy=request_proxy).text)
        except:
            multi_thread_check(IPS)
            return
        ip_info = selector.xpath("//table[@class='active']/tbody/tr")
        for i in ip_info:
            ipaddress = i.xpath('./td[1]/text()').get(default='').strip()
            port = i.xpath('./td[2]/text()').get(default='').strip()
            IP = f'{ipaddress}:{port}'
            IPS.append(IP)
        time.sleep(5)
    multi_thread_check(IPS)


def get_FateZero():
    url = f'http://proxylist.fatezero.org/proxy.list'
    logging.info(f'正在获取 {url} 的IP')
    text = get_request(url, headers=get_ua(), proxy=request_proxy).text
    IPS = []
    for i in re.findall('proxylist",(.*), "response_time":', text):
        ip_pattern = r'"host":\s+"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"'
        port_pattern = r'"port":\s+(\d+)'
        ipaddress = re.findall(ip_pattern, i)[0]
        port = re.findall(port_pattern, i)[0]
        IP = f'{ipaddress}:{port}'
        IPS.append(IP)
    multi_thread_check(IPS)


def get_xhuan_ip(url):
    selector = parsel.Selector(get_request(url, headers=get_ua(), proxy=request_proxy).text)
    ip_info = selector.xpath("//table[@class='table table-hover table-bordered']/tbody/tr")
    IPS = []
    for i in ip_info:
        ipaddress = i.xpath('./td[1]/a/text()').get(default='').strip()
        port = i.xpath('./td[2]/text()').get(default='').strip()
        IP = f'{ipaddress}:{port}'
        IPS.append(IP)
    multi_thread_check(IPS)
    neax_page_url = url + selector.xpath("//a[@aria-label='Next']/@href").get(default='')
    logging.info(f'正在获取 {neax_page_url} 的IP')
    time.sleep(5)
    return neax_page_url


def get_xhuan():
    url = 'https://ip.ihuan.me/'  # 起始url
    page = 1
    while (page < 11):
        neax_page_url = get_xhuan_ip(url)
        if neax_page_url:
            get_xhuan_ip(neax_page_url)
            page = page + 1


def get_89():
    ip_num = 200  # 想要获取的IP个数
    url = f'https://www.89ip.cn/tqdl.html?num={ip_num}&address=&kill_address=&port=&kill_port=&isp='
    logging.info(f'正在获取 {url} 的IP')
    text = get_request(url, headers=get_ua(), proxy=request_proxy).text
    pattern = r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)\b"
    ips = re.findall(pattern, text)
    print(ips)
    multi_thread_check(ips)


def get_qydl():
    urls = [f'https://proxy.ip3366.net/free/?action=china&page={PAGE}' for PAGE in range(1, 6)]
    IPS = []
    for url in urls:
        try:
            logging.info(f'正在获取 {url} 的IP')
            selector = parsel.Selector(get_request(url, headers=get_ua(), proxy=request_proxy).text)
        except:
            multi_thread_check(IPS)
            return
        ip_info = selector.xpath("//table[@class='table table-bordered table-striped']/tbody/tr")
        for i in ip_info:
            ipaddress = i.xpath('./td[1]/text()').get(default='').strip()
            port = i.xpath('./td[2]/text()').get(default='').strip()
            IP = f'{ipaddress}:{port}'
            IPS.append(IP)
        time.sleep(5)
    multi_thread_check(IPS)


def get_taiyang():
    urls = [f'http://www.taiyanghttp.com/free/page{PAGE}/' for PAGE in range(1, 6)]
    IPS = []
    for url in urls:
        try:
            logging.info(f'正在获取 {url} 的IP')
            selector = parsel.Selector(get_request(url, headers=get_ua(), proxy=request_proxy).text)
        except:
            multi_thread_check(IPS)
            return
        ip_info = selector.xpath("//div[@class='tr ip_tr']")
        for i in ip_info:
            ipaddress = i.xpath('./div[1]/text()').get(default='').strip()
            port = i.xpath('./div[2]/text()').get(default='').strip()
            IP = f'{ipaddress}:{port}'
            IPS.append(IP)
        time.sleep(5)
    multi_thread_check(IPS)


def get_xiaosu():
    main_url = 'https://www.xsdaili.cn/index.php?s=/Index/index.html'
    selector1 = parsel.Selector(get_request(main_url, headers=get_ua(), proxy=request_proxy).text)
    urls = ['https://www.xsdaili.cn' + i.xpath("./div[@class='title']/a/@href").get(default='') for i in
            selector1.xpath("//div[@class='table table-hover panel-default panel ips ']")]
    IPS = []
    for url in urls:
        try:
            logging.info(f'正在获取 {url} 的IP')
            selector = parsel.Selector(get_request(url, headers=get_ua(), proxy=request_proxy).text)
        except:
            multi_thread_check(IPS)
            return
        ip_info = selector.xpath('//div[@class="cont"]//text()').getall()
        pattern = r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)\b"
        for ip in re.findall(pattern, ''.join(ip_info)):
            IPS.append(ip)
        time.sleep(5)
    multi_thread_check(IPS)


def seofangfa():
    url = 'https://proxy.seofangfa.com/'
    IPS = []
    try:
        logging.info(f'正在获取 {url} 的IP')
        selector = parsel.Selector(get_request(url, headers=get_ua(), proxy=request_proxy, verify=False).text)
    except:
        multi_thread_check(IPS)
        return
    ip_info = selector.xpath("//table/tbody/tr")
    for i in ip_info:
        ipaddress = i.xpath('./td[1]/text()').get(default='').strip()
        port = i.xpath('./td[2]/text()').get(default='').strip()
        IP = f'{ipaddress}:{port}'
        IPS.append(IP)
    time.sleep(5)
    multi_thread_check(IPS)


def get_proxyscrape():
    url = 'https://api.proxyscrape.com/proxytable.php?nf=true&country=all'
    print(url)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, proxy={'server': 'socks5://192.168.1.171:1080'})
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        time.sleep(2)
        # context.storage_state(path="cookie.json")
        html = str(page.content())
        str_data = re.findall('<body>(.*)</body>', html)[0]
        josn_data = json.loads(str_data)
        http_data = josn_data['http']
        IPS = []
        for item in http_data:
            IPS.append(item)
        multi_thread_check(IPS)


def get_free_proxy():
    urls = [f'http://free-proxy.cz/en/proxylist/country/CN/http/ping/all/{PAGE}' for PAGE in range(1, 6)]
    IPS = []
    for url in urls:
        logging.info(f'正在获取 {url} 的IP')
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False, proxy={'server': 'socks5://192.168.1.171:1080'})
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)
            time.sleep(10)
            html = page.content()
        sel = parsel.Selector(html)
        eles = sel.xpath("//table[@id='proxy_list']//tbody/tr")
        for ele in eles:
            b64_str = ele.xpath('./td[1]/script/text()').get(default='')
            port = ele.xpath('./td[2]/span/text()').get(default='')
            if not port:
                continue
            result = re.findall(r'document\.write\(Base64\.decode\("([^"]+)"\)\)', b64_str)[0]
            host = base64.b64decode(result).decode('utf-8')
            ip = f'{host}:{port}'
            IPS.append(ip)
        time.sleep(random.randint(10, 20))
    multi_thread_check(IPS)


def get_hidemy():
    url = 'https://hidemy.io/en/proxy-list/?country=CN&type=h#list'
    command = r"C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\selenium\AutomationProfile"
    subprocess.Popen(command)  # 指定端口9922自动打开打开谷歌浏览器
    time.sleep(5)
    playwright = sync_playwright().start()
    # 连接已打开浏览器，找好端口
    browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
    default_context = browser.contexts[0]  # 注意这里不是browser.new_page()了
    page = default_context.pages[0]
    page.goto(url)
    time.sleep(30)
    page.wait_for_selector("//div[@class='table_block']//tbody/tr")
    # context.storage_state(path="cookie.json")
    html = page.content()
    sel = parsel.Selector(html)
    eles = sel.xpath("//div[@class='table_block']//tbody/tr")
    IPS = []
    for ele in eles:
        host = ele.xpath('./td[1]/text()').get(default='')
        port = ele.xpath('./td[2]/text()').get(default='')
        ip = f'{host}:{port}'
        IPS.append(ip)
        print(ip)
    multi_thread_check(IPS)


def main():
    get_zdy()
    get_ydl()
    get_kaix()
    get_kdl()
    get_89()
    get_qydl()
    get_proxyscrape()
    seofangfa()
    get_xiaosu()

    # ---------------不可用------------------
    # get_FateZero()
    # get_taiyang()
    # get_hidemy()
    # get_66()
    # get_xhuan()
    # get_free_proxy()


if __name__ == '__main__':
    main()
