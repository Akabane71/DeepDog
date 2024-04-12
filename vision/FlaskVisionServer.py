import sys
import cv2
from pyzbar import pyzbar
from flask import Flask, request, Response
import numpy as np
import QR

# 创建 Flask 应用程序实例
app = Flask(__name__)



# 初始化摄像头
try:
    cap = cv2.VideoCapture(0)
    qr = QR.QR(cap)
except Exception as e:
    print('filed open cap')
    sys.exit(1)


# 视频流
def generate_frames():
    try:
        cap = cv2.VideoCapture(0)
        while True:

            # 读取视频帧
            success, frame = cap.read()
            if not success:
                break
            else:
                # 在这里可以对视频帧进行处理，例如添加滤镜、人脸识别等

                # 将处理后的视频帧转换为字节流
                params = [cv2.IMWRITE_JPEG_QUALITY, 30]  # 质量设置为50
                ret, buffer = cv2.imencode('.jpg', frame,params)
                frame_bytes = buffer.tobytes()

                # 以字节流的形式发送视频帧
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        print('error')

# 默认视频流
@app.route(rule='/')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/qr',methods=['POST'])
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


@app.route('/YOLO',methods=['POST'])
def YOLO_vision():

    # 返回值为一个json列表 [返回的结果]
    return 'yolo'



# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
