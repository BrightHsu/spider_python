import requests
import random
import json


ip = []
with open('proxiesList.json', 'r') as f:    # 读取json文件
    for proxie in f.readlines():    # 遍历文件每行内容
        datas = json.loads(proxie)  # 行内容转换成python对象
        ip.append(datas)    # 添加到ip列表

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/73.0.3683.86 Safari/537.36'
           }

proxies = random.choice(ip)    # 随机ip
url = 'https://xin.baidu.com/'

print(proxies)
res = requests.get(url=url, headers=headers, proxies=proxies)

print(res.content.decode('utf-8'))  # 解码响应内容


