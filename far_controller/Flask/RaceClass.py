import json
import requests
import os
import struct
import threading
import time
import queue

import numpy as np
import cv2
from flask import Flask, Response


from controller import Controller



"""
    分布式节点开发! 
    实现自由共享！
"""

#
jetson_nano_host = '192.168.1.104:5000'



stop_heartbeat = False
fb_val = 10000  # 前进速度 -----> 点头摇头的速度也要变
hand_val = 20000 # 点头摇头速度
auto_fb_val = 10000  # 自动前进速度
turn_val = 10000  # 转向速度
move_val = 30000  # 平移速度
cap_number = 4  # 获取视频的
updown_val = 30000  # 点头摇头速度
stand = False  # stand 状态
cap_5 = False
cap_5_queue = queue.Queue(4)

def get_frame(num,q:queue.Queue,s):
    cap = cv2.VideoCapture(num)
    print("成功加载摄像头")
    while True:
        try:
            if q.empty():
                print("1")
                ret, frame = cap.read()
                if not ret:
                    print("放入队列")
                    q.put(frame)
            else:
                time.sleep(0.1)
        except Exception as e:
            print("cap end")
            cap.release()
            break




# 摄像头进程
cap_5_thread = threading.Thread(target=get_frame, args=(0,cap_5_queue,cap_5)).start()


# 创建 Flask 应用程序实例
app = Flask(__name__)

# 创建摄像头资源

# ----------------------------------------------------------------------------------------
# 发送一张
def capture_frame():
    print("capture_frame")
    try:
        global cap_5_queue
        global cap_5
        cap_5 = True
        t1 = time.time()
        if not cap_5_queue.empty():
            frame = cap_5_queue.get()
            cap_5 = False
            # 定义裁剪区域的坐标
            x1, y1 = 400, 200
            x2, y2 = 1600, 1300
            # 裁剪图像
            frame = frame[y1:y2, x1:x2]
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            t2 = time.time()
            print("send img total cost : ",t2-t1)
            return frame
    except Exception as e:
        print('error')

@app.route(rule='/send_img', methods=['GET'])
def send_img():
    print("send_img")
    return Response(capture_frame(), mimetype='image/jpeg')


# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
