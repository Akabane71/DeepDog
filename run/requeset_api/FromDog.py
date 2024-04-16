import requests
import json

"""
    语音播放
"""


# Dog host
host = 'http://192.168.1.101:5000'

# A B 区域
def get_area():
    url = f'{host}/qr'
    res = requests.get(url)
    res = res.text
    area = res.lower()
    return area


# 获取向左还是向右
def get_left_or_right():
    url = 'http://127.0.0.1:5000/'
    r = requests.get(url)
    data = json.loads(r.text)
    print(data)
    if data[0] == 1:
        return 'right'
    if data[1] == 1:
        return 'left'


# 指定狗播报响应的语音
def send_dz_audio(area,left_right):
    data = {
        'way':'dz',
        'area':area,
        'left_right':left_right
    }
    # 设置请求头
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(data)
    r = requests.post(url = f'{host}/audio',data=data,headers=headers)
    print(r.text)

def send_dxl_audio(area,signal,people):
    data = {
        'way': 'dxl',
        'area': area,
        'signal': signal,
        'people': people
    }
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(data)
    r = requests.post(url=f'{host}/audio', data=data,headers=headers)
    print(r.text)


if __name__ == '__main__':
    # area = 'b'
    # left_right = 'right'
    # send_dz_audio(area,left_right)
    #
    # area = 'red'
    # signal = 'fire'
    # people = '0'
    # send_dxl_audio(area,signal,people)
    print(get_area())