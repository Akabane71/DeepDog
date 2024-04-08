import os
import struct
from controller import Controller
from flask import Flask,request
import time

os.system(f'sudo clear')  # 引导用户给予root权限，避免忘记sudo运行此脚本

# global config
client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
# creat a controller
controller = Controller.Controller(server_address)



# 创建 Flask 应用程序实例
app = Flask(__name__)


@app.route(rule='/standup', methods=['GET'])
def standup():
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
    return 'end'

@app.route(rule='/forward',methods=['GET'])
def forward():
    pack = struct.pack('<3i', 0x21010130, 32600, 0)
    pass

@app.route(rule='',methods=['GET'])
def stop():

    pass

# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
