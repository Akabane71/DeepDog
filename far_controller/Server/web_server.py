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
    视频测试平台
"""


os.system(f'sudo clear')  # 引导用户给予root权限，避免忘记sudo运行此脚本

jetson_nano_host = '192.168.1.104:5000'

# 创建音频对象
a = Audio()

# 创建 Flask_give 应用程序实例
app = Flask(__name__)
# POST相关的请求
@app.route(rule='/audio_dxl', methods=['POST'])
def audio_dxl():
    if request.method == "POST":
        data = request.get_json()
        data = json.loads(data)
        area = data.get('area', '')
        people = data.get('people', '')
        signal = data.get('signal', '')
        print('area:', area)
        print('people:', people)
        print('signal:', signal)
        a.dxl(area, signal, people)
    return 'audio_dxl'

@app.route(rule='/audio_dz', methods=['POST'])
def audio_dxl():
    if request.method == "POST":
        data = request.get_json()
        data = json.loads(data)
        area = data.get('area', '')
        left_right = data.get('left_right', '')
        a.dxl(area, left_right)
    return 'audio_dz'

@app.route(rule='/qr', methods=['POST'])
def qr():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
    except Exception as e:
        return 'error: no cap'
    for i in range(200):
        res = qr.go()
        if res:
            return res
    return 'error: no'


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
