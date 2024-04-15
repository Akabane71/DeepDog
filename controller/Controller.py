import os
import socket
import struct
import sys
import threading
import time


class Controller:
    def __init__(self, dst):
        self.lock = False
        self.last_ges = "stop"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dst = dst

    # used to send a pack to robot dog
    def send(self, pack):
        self.socket.sendto(pack, self.dst)

