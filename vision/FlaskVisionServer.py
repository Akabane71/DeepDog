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
    try:
        ret, frame = cap.read()
    except Exception as e:
        return 'error: no cap'
    qr_list = []
    while True:
        cv2.imshow('frame',frame)
        if not ret:
            return 'NO CAP'
        else:
            qrcodes = pyzbar.decode(frame)
            if qrcodes:
                for obj in qrcodes:
                    print('Data:', obj.data.decode('utf-8'))
                    decoded_data = obj.data.decode('utf-8')
                    qr_list.append(decoded_data)
            if len(qr_list) > 3:
                if qr_list[0] == qr_list[1] == qr_list[2]:
                    print('res:', qr_list[0])
                    break
                else:
                    qr_list.pop(0)
                return qr_list[0]


@app.route('/YOLO',methods=['GET'])
def YOLO_vision():

    # 返回值为一个json列表 [返回的结果]
    return 'yolo'



# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
