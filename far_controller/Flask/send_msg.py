import threading
import requests

dog_host = ''
import json
def go_get(host,u):
    url = f'http://{host}/{u}'
    r = requests.get(url)
    print(r.text)

# 多进程发送
def go_get_thread(host,u):
    threading.Thread(target=go_get, args=(host, u)).start()

def go_stand_up():
    url = f'http://192.168.1.101:5000/standup'
    r = requests.get(url)
    print(r.text)

