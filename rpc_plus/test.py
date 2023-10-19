

from rpc_plus.rpc_client import RpcClient
from concurrent.futures import ThreadPoolExecutor


rpc_client = RpcClient('localhost', 5378, 'test')

with ThreadPoolExecutor() as p:
    def back(res):
        r = res.result()
        print(r.type, r.status_code)
        print(r.content)

    for i in range(1):
        rpc_data = {'url': 'https://royalsocietypublishing.org/doi/pdf/10.1098/rsta.2022.0209'}

        p.submit(rpc_client.run, 'requestGet', rpc_data).add_done_callback(back)
        # res = rpc_client.run('requestGet', rpc_data)

