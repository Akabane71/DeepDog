import time
import struct
import threading
import os
import psutil
from controller import Controller

os.system(f'sudo clear')  # 引导用户给予root权限，避免忘记sudo运行此脚本

# global config
client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)

# 让狗的生命一直启动
def go(con):
    try:
        print('Ctrl + c 结束运行')
        pack = struct.pack('<3i', 0x21040001, 0, 0)
        while True:
            con.send(pack)
            time.sleep(0.25)  # 4Hz
    except KeyboardInterrupt as e:
        print('结束运行')

if __name__ == '__main__':
    # creat a controller
    controller = Controller.Controller(server_address)
    go(controller)
