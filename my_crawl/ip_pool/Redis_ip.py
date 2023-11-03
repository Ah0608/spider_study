import logging
import random
import redis


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class ProxyPool():
    def __init__(self, host='localhost', port=6379,db=0):
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
