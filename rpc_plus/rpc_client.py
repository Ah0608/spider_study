# -*- coding: utf-8 -*-
# @Author  : xiao lin
# @Project : rpc_plus
# @File    : rpc_client.py
# @Soft    : PyCharm
# @Time    : 2023/9/16 11:40
# @Desc    :
import re
import time
import asyncio
import json
import websockets
import magic
from typing import Union


class RpcResponse:
    status_code: int = 200
    type: str
    content: bytes = b''
    text: str = ''
    json: dict = None


class RpcClient:
    def __init__(self, host: str, port: Union[str, int] = 5378,
                 group: str = None,
                 timeout: int = 10,
                 max_timeout: int = 60*5):
        self.host = host
        self.port = port
        if not group:
            raise AttributeError('The group parameter is required.')
        self.group = group
        self.timeout = timeout  # 浏览器刷新的等待时间
        self.max_timeout = max_timeout  # 最大等待超时时间

    async def __connect(self, action: str, data: dict) -> RpcResponse:
        url = f"ws://{self.host}:{self.port}/invoke?group={self.group}&action={action}"
        message = {'group': self.group, 'action': action}
        async with websockets.connect(url, max_size=2 ** 32) as websocket:
            message.update(data)
            message = json.dumps(message)
            await websocket.send(message)
            try:
                timeout = self.timeout if action == 'reload' else self.max_timeout
                response = await asyncio.wait_for(websocket.recv(), timeout=timeout)
                if isinstance(response, bytes):
                    res = RpcResponse()
                    res.type = 'byte'
                    res.content = response
                    detect_info = self.detect_file_type(response)
                    if 'HTML' in detect_info or 'SGML' in detect_info:
                        res.text = response.decode(re.findall(r',\s+(.*?)\s+', detect_info)[0])
                    return res
                else:
                    res = RpcResponse()
                    res_text = json.loads(response)['data']
                    status = json.loads(response)['status']
                    if status == '-1':
                        res.type = 'str'
                        res.text = res_text
                        res.status_code = -1
                        return res
                    if isinstance(res_text, str):
                        res.type = 'str'
                        res.text = res_text
                    else:
                        res.type = 'json'
                        res.json = res_text
                    return res
            except asyncio.TimeoutError:
                res = RpcResponse()
                res.type = 'str'
                res.text = f'{action}--运行已超时！！'
                res.status_code = -1
                return res

    def run(self, action: str, data: dict) -> RpcResponse:
        return asyncio.run(self.__connect(action, data))

    def reload(self, sleep=None, logger=None):
        """
        刷新浏览器，用的是js里的location.reload();
        :param sleep: 时间间隔
        :param logger: 日志对象
        :return:
        """
        if not sleep:
            sleep = self.timeout // 2

        self.run('reload', {})
        while True:
            time.sleep(sleep)
            res = self.run('getState', {})
            if res.type == 'str' and res.status_code == 200 and '刷新成功' in res.text:
                if logger:
                    logger.info('刷新成功！！')
                else:
                    print('刷新成功！！')
                return
            if logger:
                logger.info(f'等待{sleep}s后刷新！')
            else:
                print(f'等待{sleep}s后刷新！')

    @staticmethod
    def detect_file_type(blob):
        # 创建一个Magic对象
        file_magic = magic.Magic()
        # 检测文件类型
        file_type = file_magic.from_buffer(blob)
        return file_type

    # 下面是老代码
    # rpc_client.run('reload', {})
    # while True:
    #     res = rpc_client.run('getState', {})
    #     if res.type == 'str' and res.status_code == 200 and '刷新成功' in res.text:
    #         if logger:
    #             logger.info('刷新成功！！')
    #         else:
    #             print('刷新成功！！')
    #         break
    #     time.sleep(sleep)
    #     if logger:
    #         logger.info(f'等待{sleep}后刷新！')
    #     else:
    #         print(f'等待{sleep}后刷新！')


if __name__ == '__main__':
    c = RpcClient('localhost', 5378, 'apsChrome166')
    da = {
        'url': 'https://iopscience.iop.org/article/10.1088/1755-1315/1240/1/011001',
    }
    r = c.run('getState', da)
    print(r.type)
