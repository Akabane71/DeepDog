import sys
import time
import struct
import threading
import os
import psutil
from controller import Controller


# os.system(f'sudo clear')  # 引导用户给予root权限，避免忘记sudo运行此脚本

# global config
client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)

# creat a controller
controller = Controller.Controller(server_address)

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

print("Waiting 5s......")
time.sleep(5)
# 转圈
print("Rotating...")
controller.send(struct.pack('<3i', 0x21010135, 13000, 0))
time.sleep(3)  # need time to turn 360 degrees
controller.send(struct.pack('<3i', 0x21010135, 0, 0))
time.sleep(5)
print(4)
controller.send(pack)




