import sys
import cv2
from pyzbar import pyzbar
from flask import Flask,request
import numpy as np
import QR

# 创建 Flask 应用程序实例
app = Flask(__name__)

# 初始化摄像头
try:
    cap = cv2.VideoCapture(0)
except Exception as e:
    print('filed open cap')
    sys.exit(1)

qr = QR.QR(cap)


# 定义一个简单的路由
@app.route('/',methods=['GET'])
def hello_world():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        return data
    return 'Hello, World!'
@app.route('/qr',methods=['GET'])
def QR_vision():
    try:
        ret, frame = cap.read()
    except Exception as e:
        return 'error: no cap'
    for i in range(200):
        res = qr.go()
        if res:
            return res
    return 'error: no'



@app.route('/YOLO',methods=['GET'])
def YOLO_vision():

    # 返回值为一个json列表 [返回的结果]
    return 'yolo'



# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
