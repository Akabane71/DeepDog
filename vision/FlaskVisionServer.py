import sys
import cv2
from pyzbar import pyzbar
from flask import Flask,request
import numpy as np

# 创建 Flask 应用程序实例
app = Flask(__name__)

# 初始化摄像头
try:
    cap = cv2.VideoCapture(0)
except Exception as e:
    print('filed open cap')
    sys.exit(1)




# 定义一个简单的路由
@app.route('/',methods=['GET'])
def hello_world():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        return data
    return 'Hello, World!'
@app.route('/QR',methods=['GET'])
def QR_vision():
    ret, frame = cap.read()
    while True:
        cv2.imshow('frame',frame)
        if not ret:
            return 'NO CAP'
        else:
            decoded_objects = pyzbar.decode(frame)
            # 存储解码结果的字符串
            decoded_data = ""
            for obj in decoded_objects:
                decoded_data += f"{obj.data.decode('utf-8')}\n\n"
            return decoded_data

@app.route('/YOLO',methods=['GET'])
def YOLO_vision():

    # 返回值为一个json列表 [返回的结果]
    return 'yolo'



# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
