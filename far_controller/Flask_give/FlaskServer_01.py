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
    一直往前走的版本
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
fb_val = 22600  # 前进速度
turn_val = 10000 # 转向速度
move_val = 30000 # 平移速度
cap_number = 0

# start to exchange heartbeat pack
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

# 创建 Flask_give 应用程序实例
app = Flask(__name__)


# GET相关的请求
@app.route(rule='/standup', methods=['GET'])
def standup():
    # stand up
    pack = struct.pack('<3i', 0x21010202, 0, 0)
    controller.send(pack)
    print('stand up')
    time.sleep(1)
    return 'dog stand up!'

# ------------------------------
#   前进
@app.route(rule='/forward', methods=['GET'])
def forward():
    pack = struct.pack('<3i', 0x21010130, fb_val, 0)
    controller.send(pack)
    return 'dog forward'
@app.route(rule='/back', methods=['GET'])
def back():
    pack = struct.pack('<3i', 0x21010130, -fb_val, 0)
    controller.send(pack)
    return 'dog back'
@app.route(rule='/stop_fb', methods=['GET'])
def stop_fb():
    pack = struct.pack('<3i', 0x21010130, 0, 0)
    controller.send(pack)
    return 'dog stop fb'


# -----------------------------------------------
#   转向
@app.route(rule='/turn_left', methods=['GET'])
def turn_left():
    pack = struct.pack('<3i', 0x21010135, -turn_val, 0)
    controller.send(pack)
    return 'dog left'
@app.route(rule='/turn_right', methods=['GET'])
def turn_right():
    pack = struct.pack('<3i', 0x21010135, turn_val, 0)
    controller.send(pack)
    return 'dog right'
@app.route(rule='/stop_turn', methods=['GET'])
def stop_turn():
    pack = struct.pack('<3i', 0x21010135, 0, 0)
    controller.send(pack)
    return 'dog stop turn'


# ------------------------------------------------
#  左右平移
@app.route(rule='/move_left', methods=['GET'])
def move_left():
    pack = struct.pack('<3i', 0x21010131, -move_val, 0)
    controller.send(pack)
    return 'dog move left'
@app.route(rule='/move_right', methods=['GET'])
def move_right():
    pack = struct.pack('<3i', 0x21010131, move_val, 0)
    controller.send(pack)
    return 'dog move right'
@app.route(rule='/stop_move', methods=['GET'])
def stop_move():
    pack = struct.pack('<3i', 0x21010131, 0, 0)
    controller.send(pack)
    return 'dog stop move'

# ----------------------------------------------------------------------------------------
#   模式切换
@app.route(rule='/stop_heart', methods=['GET'])
def stop_heart():
    global stop_heartbeat
    stop_heartbeat = True
    return 'dog heart_stop'
@app.route(rule='/re_heart', methods=['GET'])
def re_heart():
    global stop_heartbeat
    stop_heartbeat = False
    return 'dog restart'

# -------------------------
# 楼梯姿态
@app.route(rule='/ladder', methods=['GET'])
def change_to_ladder():
    pack = struct.pack('<3i', 0x21010401, 0, 0)
    controller.send(pack)
    return 'dog change to ladder'
# 行走姿态
@app.route(rule='/walk', methods=['GET'])
def change_to_walk():
    pack = struct.pack('<3i', 0x21010300, 0, 0)
    controller.send(pack)
    return 'dog change to walk'
# 跑步姿态
@app.route(rule='/run', methods=['GET'])
def change_to_run():
    pack = struct.pack('<3i', 0, 0, 0)
    controller.send(pack)
    return 'doge change to run'



@app.route(rule='/clear', methods=['GET'])
def clear():
    pack = struct.pack('<3i', 0x21010C05, 0, 0)
    controller.send(pack)
    return 'dog clear'


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
    return 'dog audio'

@app.route(rule='/qr', methods=['GET'])
def qr():
    url = f'http://{jetson_nano_host}/qr'
    response = requests.get(url)
    data = response.text
    print(data)
    return data


# ----------------------------------------------------------------------------------------

# 改变摄像头
@app.route(rule='/change_cap', methods=['GET'])
def change_cap():
    global cap_number
    if cap_number == 0:
        cap_number = 4
    else:
        cap_number = 0
    return 'dog cap changed'

# 生成视频流
def generate_frames():
    try:
        cap = cv2.VideoCapture(cap_number)
        while True:
            # 读取视频帧
            success, frame = cap.read()
            if not success:
                break
            else:
                # 在这里可以对视频帧进行处理，例如添加滤镜、人脸识别等

                # params = [cv2.IMWRITE_JPEG_QUALITY, 50]  # 质量设置为50
                # 将处理后的视频帧转换为字节流
                ret, buffer = cv2.imencode('.jpg', frame,params)
                frame_bytes = buffer.tobytes()

                # 以字节流的形式发送视频帧
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        print('error')


@app.route(rule='/')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
