import threading
import requests
import json
import struct
import time

from Controller import Controller
client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
class GO():
    def __init__(self,server_address):
        self.con = Controller(server_address)

    @staticmethod
    def heart_exchange(con):
        pack = struct.pack('<3i', 0x21040001, 0, 0)
        while True:
            con.send(pack)
            time.sleep(0.25)  # 4Hz

    # 隐藏的方法
    def send(self,msg,val=0):
        pack = struct.pack('<3i', msg, val, 0)
        self.con.send(pack)

    # 发送指令
    def go(self,msg,val=0):
        threading.Thread(target=self.send,args=(msg,val,)).start()


