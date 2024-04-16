import threading

import requests
import json
def go_get(host,u):
    url = f'http://{host}/{u}'
    r = requests.get(url)
    print(r.text)

# 多进程发送
def go_get_thread(host,u):
    threading.Thread(target=go_get, args=(host, u)).start()

def go_audio(host,u,a='red',p='one',s='fire'):
    data = {
        'area':a,
        'people':p,
        'signal':s
    }
    data = json.dumps(data)

    url = f'http://{host}/{u}'
    r = requests.post(url,data=data)
    print(r.text)
    # 后续解析返回一个数值
