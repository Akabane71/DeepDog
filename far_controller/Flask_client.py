import time

import requests
import json
def go(s,way):
    url = f'http://192.168.1.101:5000/{s}'
    data = {
        'area':'red',
        'people':'one',
        'signal':'fire'
    }
    data = json.dumps(data)
    if way == 'post':
        response = requests.post(url,json=data)
        print(response.text)
    else:
        response = requests.get(url, json=data)
        print(response.text)

if __name__ == '__main__':
    go('standup','get')
    time.sleep(1)

    go('forward','get')

    go('back','get')

    go('audio','post')

    go('left','post')

    go('right','post')
    time.sleep(1)

    go('stop','get')
    time.sleep(2)

    time.sleep(3)
    go('clear','get')
    # go('stop_heart','get')
    #
    # go('re_heart','get')

