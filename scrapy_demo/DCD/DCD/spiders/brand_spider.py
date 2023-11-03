#
# import requests
#
# from my_crawl.tool.utils import get_ua
#
#
# def get_ip():
#     # data = requests.get(url='https://dps.kdlapi.com/api/getdps/?secret_id=o3xsbuahej0brfuwxwxl&num=5&signature=ooh2gl5o6taghr3pacfvieq3l1&pt=1&sep=%2C').text
#     # ips = []
#     # for i in data.split(','):
#     #     ips.append('http://d3887508130:5y0l28oa@{}'.format(i))
#     # print(ips)
#     ips = ['http://192.168.1.171:8118',
#            'http://192.168.1.183:38118',
#            'http://111.177.63.86:8888',
#            'http://106.11.226.232:8009',
#            'http://117.71.112.190:8888',
#            'http://139.224.67.166:7890',
#            ]
#     for ip in ips:
#             proxy = {"http": f"{ip}", "https": f"{ip}"}
#             REQUEST_URL = 'https://www.dongchedi.com'
#             response = requests.get(REQUEST_URL, proxies=proxy, headers=get_ua(), timeout=10)
#             print(response.status_code)
#
# if __name__ == '__main__':
#     get_ip()