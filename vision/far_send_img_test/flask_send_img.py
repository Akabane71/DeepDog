import time

from flask import Flask, Response
import cv2

app = Flask(__name__)

# 发送一张图片
def capture_frame():
    t0 = time.time()
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    camera.release()
    if success:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        t2 = time.time()
        print('total time: ' + str(t2 - t0))
        return frame

@app.route('/')
def index():
    return Response(capture_frame(), mimetype='image/jpeg')

# camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
# camera.set(cv2.CAP_PROP_FPS,60)
# camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

if __name__ == "__main__":
    app.run('0.0.0.0',debug=True)
