from flask import Flask, Response
import cv2

app = Flask(__name__)

# 发送一张图片
def capture_frame():
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    # 使用完要及时释放
    camera.release()
    if success:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return frame

@app.route('/')
def index():
    return Response(capture_frame(), mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True)
