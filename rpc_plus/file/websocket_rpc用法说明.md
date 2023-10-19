[toc]
# 基于WebSocket和RPC的网络请求方法使用说明


### 更新日志
2023-10-12 
	rpc_server.py文件 93行
	修改前：msg.split(b'---')， 修改后：msg.split(b'=-=+=', 1)，
	template.js文件 149行
	var newBlob = prependStringToBlob(response, seq + '---'); var newBlob = prependStringToBlob(response, seq + '=-=+=');
	原因：
	之前用的是---, 会导致es下载下来的PDF文件用wps打不开，但是文件是正确的，现在改为=-=+=
	
2023-09-25 rpc_client.py文件 53行
	```python
	# 修改前
	if 'HTML' in detect_info:
	res.text = response.decode(re.findall(r',\s+(.*?)\s+', detect_info)[0])
	# 修改后
	if 'HTML' in detect_info or 'SGML' in detect_info:
	res.text = response.decode(re.findall(r',\s+(.*?)\s+', detect_info)[0])
	```
	原因：
	使用了magic模块来检测文件的类型， SGML是THML的基类，之前没有检测到
	

### 一、 项目概述
项目名称： rpc_plus, 版本1.0 

本项目是基于websocket通信和rpc思想的网络请求方法， 使用python和JavaScript通过websocket通信，用远程调用的思想，使得python端可以控制JavaScript的代码执行，
达到用浏览器环境发送网络请求的目的。大部分网站都有很严格的反爬措施，用一般的python请求库(如requests，httpx，aiohttp， pycurl)或自动化工具（如selenium，playwright），
由于python的库都不支持定制tls指纹，有的还不支持HTTP2，自动化工具又有很明显的指纹，所以很容易就被网站检测到从而被反爬或封禁。于是，本项目在这种情况诞生，直接在浏览器
环境发请求和操作浏览器，不容易触发网站的反爬限制，因为网站需要支持普通用户的使用，不可能对真实浏览做过多反爬限制，除非请求过快。


### 二、 文件构成
提供压缩包，解压缩后，是如下文件内容。

requirement.txt   -->  需要安装python库

log_manager.py    -->  日志模块（非必须）

rpc_client.py     -->  rpc客户端

rpc_server.py     -->  rpc服务端

template.js		  -->  需要注入到浏览器环境作为JavaScript websocket客户端的JavaScript文件模板


### 三、 安装与环境
安装：在cmd中pip install -r requirements.txt
环境：需要python3.8及以上

**注意**：我用的是python3.10.10，其他版本没测试过

### 四、 用法详解
依赖库和环境配置好以后， 按如下步骤运行。
1. 运行rpc_server.py文件，启动websocket服务
2. 把template.js注入到已经登录了账号或准备好的浏览器。注入方式有如下几种。
	- 直接在控制台注入，打开浏览器的开发者工具的控制台，把代码粘贴后回车即可。优点是快捷，缺点是每次都需要手动注入。
	- 油猴脚本注入，把第6行的@match后面的网站修改为目标网址，注意*号，这是为了只匹配目标网址，以免影响其他网站的运行。
		当然，也可多写几个网址。优点是方便，一劳永逸，缺点是需要安装油猴脚本插件。
	
	**注意事项：**
	- 需要修改212行里url的group参数，不同的项目可能有不同的事件和响应，最好不同项目用不同的group。
	- 然后下面registerAction函数可以注册不同action，可根据自己的项目自定义action并注册。
3. 在需要发送请求的文件导入rpc_client.py 里的 RpcClient 类
例：
```python
from rpc_client import RpcClient 

rpc_client = RpcClient('localhost', 5378, 'esFireFox102')
rpc_data = {'url': url}
res = rpc_client.run('browserGetPdf', rpc_data)
```
RpcClient类有两个方法，

一是这个run()， 表示要运行什么动作去操控浏览器

参数1：类型是字符串，表示要触发JavaScript的动作，此动作可自定义

参数2：类型是字典，传递到动作函数里的参数，通常是url

返回值： 这里run返回的res是一个RpcResponse对象，包含属性有：

type：表示返回的类型，只有str 和 byte

status_code： 表示执行状态， 只有200和-1，成功是200，否则-1

content： 表示返回的二进制

text： 表示返回的文本，可能是网页的文本和错误信息

json： 表示返回的json信息

方法二是reload()，表示刷新浏览器
参数1：int， 延迟时间， 参数2：logger，用于日志，都有默认值，可不传。
无返回值
	
### 五、参考连接
参考了这个项目：https://github.com/sixgad/py-jsrpc 

油猴官网：https://www.tampermonkey.net 