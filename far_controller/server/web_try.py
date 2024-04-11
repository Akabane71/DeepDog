import json
import os
import struct
import threading
import time

import cv2
from flask import Flask, request,Response
import requests

from audio.Audio import Audio
from controller import Controller

"""
    向前走一步的版本

"""


os.system(f'sudo clear')  # 引导用户给予root权限，避免忘记sudo运行此脚本

#
jetson_nano_host = '192.168.1.104:5000'

# global config
client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
# creat a controller
controller = Controller.Controller(server_address)

stop_heartbeat = False


# 心跳开启
def heart_exchange(con):
    pack = struct.pack('<3i', 0x21040001, 0, 0)
    while True:
        if stop_heartbeat:
            break
        con.send(pack)
        time.sleep(0.25)  # 4Hz
heart_exchange_thread = threading.Thread(target=heart_exchange, args=(controller,))
heart_exchange_thread.start()

# 创建音频对象
a = Audio()

# 创建 Flask 应用程序实例
app = Flask(__name__)


# GET相关的请求
@app.route(rule='/standup', methods=['GET'])
def standup():
    # stand up
    pack = struct.pack('<3i', 0x21010202, 0, 0)
    print(1)
    controller.send(pack)
    return 'stand up!'


@app.route(rule='/forward', methods=['GET'])
def forward():
    pack = struct.pack('<3i', 0x21010130, 22600, 0)
    controller.send(pack)
    time.sleep(0.1)
    pack = struct.pack('<3i', 0x21010130, 0, 0)
    controller.send(pack)
    return 'forward'


@app.route(rule='/back', methods=['GET'])
def back():
    pack = struct.pack('<3i', 0x21010130, -22600, 0)
    controller.send(pack)
    time.sleep(0.1)
    pack = struct.pack('<3i', 0x21010130, 0, 0)
    controller.send(pack)
    return 'back'

@app.route(rule='/left', methods=['GET'])
def turn_left():
    pack = struct.pack('<3i', 0x21010135, -10000, 0)
    controller.send(pack)
    time.sleep(0.1)
    pack = struct.pack('<3i', 0x21010135, 0, 0)
    controller.send(pack)
    return 'left'

@app.route(rule='/right', methods=['GET'])
def turn_right():
    pack = struct.pack('<3i', 0x21010135, 12600, 0)
    controller.send(pack)
    time.sleep(0.1)
    pack = struct.pack('<3i', 0x21010135, 0, 0)
    controller.send(pack)
    return 'right'

@app.route(rule='/stop_heart', methods=['GET'])
def stop_heart():
    global stop_heartbeat
    stop_heartbeat = True
    return 'dog stop'

@app.route(rule='/ladder', methods=['GET'])
def change_to_ladder():
    pack = struct.pack('<3i', 0, 0, 0)
    controller.send(pack)
    return 'change to ladder'


@app.route(rule='/run', methods=['GET'])
def change_to_run():
    """
    :return:
    """
    pack = struct.pack('<3i', 0, 0, 0)
    controller.send(pack)
    return 'change to run'

@app.route(rule='/re_heart', methods=['GET'])
def re_heart():
    global stop_heartbeat
    stop_heartbeat = False
    return 'dog restart'


@app.route(rule='/clear', methods=['GET'])
def clear():
    pack = struct.pack('<3i', 0x21010C05, 0, 0)
    controller.send(pack)
    return 'clear'


# POST相关的请求
@app.route(rule='/audio', methods=['POST'])
def audio():
    if request.method == "POST":
        data = request.get_json()
        data = json.loads(data)
        area = data.get('area', '')
        people = data.get('people', '')
        signal = data.get('signal', '')
        print('area:', area)
        print('people:', people)
        print('signal:', signal)
        a.go(area, signal, people)
    return 'audio'

@app.route(rule='/qr', methods=['POST'])
def qr():
    url = f'http://{jetson_nano_host}/qr'
    response = requests.get(url)
    data = response.text
    print(data)
    return data


# ----------------------------------------------------------------------------------------

# 将摄像头封装成视频流
def generate_frames():
    global vision_sign
    try:
        cap = cv2.VideoCapture(0)
        while True:

            # 读取视频帧
            success, frame = cap.read()
            if not success:
                break
            else:
                # 在这里可以对视频帧进行处理，例如添加滤镜、人脸识别等

                # 将处理后的视频帧转换为字节流
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()

                # 以字节流的形式发送视频帧
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        print('error')


@app.route(rule='/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
