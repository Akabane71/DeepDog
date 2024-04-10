import json
import os
import struct
import threading

from controller import Controller
from flask import Flask, request
import time

from audio.Audio import Audio

# os.system(f'sudo clear')  # 引导用户给予root权限，避免忘记sudo运行此脚本

# global config
client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
# creat a controller
controller = Controller.Controller(server_address)

stop_heartbeat = False

# start to exchange heartbeat pack
def heart_exchange(con):
    pack = struct.pack('<3i', 0x21040001, 0, 0)
    while True:
        if stop_heartbeat:
            return
        con.send(pack)
        time.sleep(0.25)  # 4Hz
heart_exchange_thread = threading.Thread(target=heart_exchange, args=(controller,))
heart_exchange_thread.start()

# 创建音频对象
a = Audio()

# 创建 Flask 应用程序实例
app = Flask(__name__)


standup_num = 0

@app.route(rule='/standup', methods=['GET'])
def standup():
    global standup_num
    # 第一次启动
    if standup_num == 0:
        # stand up
        pack = struct.pack('<3i', 0x21010202, 0, 0)
        print(1)
        controller.send(pack)
        time.sleep(3)
        print(2)
        controller.send(pack)
        time.sleep(3)
        print(3)
        controller.send(pack)
    else:
        standup_num += 1
        pack = struct.pack('<3i', 0x21010202, 0, 0)
        print(1)
        controller.send(pack)
        time.sleep(3)
    return 'stand up!'


@app.route(rule='/stop', methods=['GET'])
def stop():
    pack = struct.pack('<3i', 0x21010202, 0, 0)
    controller.send(pack)
    return 'stop!'


@app.route(rule='/forward', methods=['GET'])
def forward():
    pack = struct.pack('<3i', 0x21010130, 32600, 0)
    controller.send(pack)
    time.sleep(3)
    pack = struct.pack('<3i', 0x21010130, 0, 0)
    controller.send(pack)
    return 'forward'


@app.route(rule='/back', methods=['GET'])
def back():
    pack = struct.pack('<3i', 0x21010130, -12600, 0)
    controller.send(pack)
    time.sleep(1)
    pack = struct.pack('<3i', 0x21010130, 0, 0)
    controller.send(pack)
    return 'back'


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


@app.route(rule='/left', methods=['POST'])
def turn_left():
    pack = struct.pack('<3i', 0x21010135, 22600, 0)
    controller.send(pack)
    time.sleep(2)
    pack = struct.pack('<3i', 0x21010135, 0, 0)
    controller.send(pack)
    return 'left'

@app.route(rule='/right', methods=['POST'])
def turn_right():
    pack = struct.pack('<3i', 0x21010135, -22600, 0)
    controller.send(pack)
    time.sleep(2)
    pack = struct.pack('<3i', 0x21010135, 0, 0)
    controller.send(pack)
    return 'right'

@app.route(rule='/stop_heart', methods=['GET'])
def stop_heart():
    global stop_heartbeat
    stop_heartbeat = True
    return 'dog stop'

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




# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)