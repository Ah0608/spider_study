import kdl

from my_crawl.ip_pool.Redis_ip import ProxyPool


class kdl_proxy(object):
    def __init__(self):
        self.SecretId = "ohclai4hltu4vsaninyb"
        self.SecretKey = "0j45hogaii12xvl7yd4dvf701g5gn1f8"
        self.username = "d2529332024"
        self.password = "5y0l28oa"
        self.auth = kdl.Auth(self.SecretId, self.SecretKey)
        self.client = kdl.Client(self.auth)
        self.host = 'localhost'
        self.port = 6379
        self.db = 1
        self.proxypool = ProxyPool(self.host,self.port,self.db)

    def get_order_expire_time(self):
        # 获取订单到期时间, 返回时间字符串
        expire_time = self.client.get_order_expire_time()
        print("您的订单到期时间截止为：", expire_time)

    def get_ip_whitelist(self):
        # 获取ip白名单, 返回ip列表
        ip_whitelist = self.client.get_ip_whitelist()
        list_num = len(ip_whitelist)
        print('您设置的ip白名单共有{}个,分别为:\r'.format(list_num))
        for ip_white in ip_whitelist:
            print(ip_white)

    def set_ip_whitelist(self,ip_list):
        # 设置ip白名单，参数类型为字符串或列表或元组
        # 成功则返回True, 否则抛出异常
        state = self.client.set_ip_whitelist(ip_list)
        if state is True:
            print('ip白名单设置成功！')
            self.get_ip_whitelist()
        else:
            print('ip白名单设置失败！')

    def check_ip_valid(self,ips):
        # 检测私密代理有效性： 返回 ip: true/false 组成的dict
        valids = self.client.check_dps_valid(ips)
        return valids

    def get_ips(self,ip_num,return_format='json',ip_type=1,ip_area=None):
        '''
        :param ip_num: 指定想要获取的ip数量
        :param return_format: 指定返回的内容格式 text、json、xml
        :param ip_type: 指定代理ip类型 1: http代理(默认) 2: socks代理
        :param ip_area: 指定ip的地区 例：北京或110000
        :return:
        '''
        # 具体有哪些参数请参考帮助中心: "https://www.kuaidaili.com/doc/api/getdps/"
        ips = self.client.get_dps(num=ip_num,format=return_format, pt=ip_type,area=ip_area)
        ip_num = len(ips)
        for ip in ips:
            valids = self.check_ip_valid(ip)
            if valids[ip] is True:
                print(ip)
                proxies = f"{self.username}:{self.password}@{ip}"
                self.proxypool.add_proxy(proxies,100)
        print(f'您共获取到{ip_num}个代理!并将以上代理添加到host为:{self.host} port为:{self.port} db为:{self.db}的Redis数据库中')

    def get_ip_valid_time(self,ips):
        # 获取私密代理剩余时间: 返回 ip: seconds(剩余秒数) 组成的dict
        seconds = self.client.get_dps_valid_time(ips)
        time = seconds[ips]
        minutes = time // 60
        seconds = time % 60
        print(f'代理:{ips}剩余{minutes}分{seconds}秒。')

    def get_ip_balance(self):
        # 获取计数版ip余额（仅私密代理计数版）
        balance = self.client.get_ip_balance(sign_type='hmacsha1')
        print("您账户的私密ip余额个数为", balance)


if __name__ == '__main__':
    kdl = kdl_proxy()
    kdl.get_ip_balance()






