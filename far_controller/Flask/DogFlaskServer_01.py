import json
import requests
import os
import struct
import threading
import time

import numpy as np
import cv2
from flask import Flask, Response, request

from audio.Audio import Audio
from controller import Controller
from qr import QR
from vision import WhiteFindGreyDIY, BlackFindGrayDIY
from vision.do import white_90, black_stair

"""
    一直往前走的版本,正式版本
"""

os.system(f'sudo clear')  # 引导用户给予root权限，避免忘记sudo运行此脚本

#
jetson_nano_host = '192.168.1.104:5000'

# global config
client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
# creat a controller
controller = Controller.Controller(server_address)

stop_heartbeat = False
fb_val = 20000  # 前进速度
auto_fb_val = 10000  # 自动前进速度
turn_val = 10000  # 转向速度
move_val = 30000  # 平移速度
cap_number = 4  # 获取视频的
updown_val = 30000  # 点头摇头速度
stand = False  # stand 状态


# start to exchange heartbeat pack
def heart_exchange(con):
    pack = struct.pack('<3i', 0x21040001, 0, 0)
    while True:
        if stop_heartbeat:
            print('dog stop heart!')
            time.sleep(0.25)
            continue
        con.send(pack)
        time.sleep(0.25)  # 4Hz


heart_exchange_thread = threading.Thread(target=heart_exchange, args=(controller,))
# 开启守护进程
# heart_exchange_thread.daemon = True
# heart_exchange_thread.start()

# 创建音频对象
a = Audio()
# 创建qr码识别对象
q = QR.QR()

# 创建 Flask 应用程序实例
app = Flask(__name__)


@app.route(rule='/standup', methods=['GET'])
def standup():
    # stand up
    pack = struct.pack('<3i', 0x21010202, 0, 0)
    controller.send(pack)
    print('stand up')
    time.sleep(2)
    return 'dog stand up!'


# ----------------------------------------------------------------
#   前进
@app.route(rule='/forward', methods=['GET'])
def forward():
    pack = struct.pack('<3i', 0x21010130, fb_val, 0)
    controller.send(pack)
    return 'dog forward'


@app.route(rule='/back', methods=['GET'])
def back():
    pack = struct.pack('<3i', 0x21010130, -fb_val, 0)
    controller.send(pack)
    return 'dog back'


@app.route(rule='/stop_fb', methods=['GET'])
def stop_fb():
    pack = struct.pack('<3i', 0x21010130, 0, 0)
    controller.send(pack)
    return 'dog stop fb'


# -----------------------------------------------
#   转向
@app.route(rule='/turn_left', methods=['GET'])
def turn_left():
    pack = struct.pack('<3i', 0x21010135, -turn_val, 0)
    controller.send(pack)
    return 'dog left'


@app.route(rule='/turn_right', methods=['GET'])
def turn_right():
    pack = struct.pack('<3i', 0x21010135, turn_val, 0)
    controller.send(pack)
    return 'dog right'


@app.route(rule='/stop_turn', methods=['GET'])
def stop_turn():
    pack = struct.pack('<3i', 0x21010135, 0, 0)
    controller.send(pack)
    return 'dog stop turn'


# ------------------------------------------------
#  左右平移
@app.route(rule='/move_left', methods=['GET'])
def move_left():
    pack = struct.pack('<3i', 0x21010131, -move_val, 0)
    controller.send(pack)
    return 'dog move left'


@app.route(rule='/move_right', methods=['GET'])
def move_right():
    pack = struct.pack('<3i', 0x21010131, move_val, 0)
    controller.send(pack)
    return 'dog move right'


@app.route(rule='/stop_move', methods=['GET'])
def stop_move():
    pack = struct.pack('<3i', 0x21010131, 0, 0)
    controller.send(pack)
    return 'dog stop move'


# ---------------------------------------------------
# 上下
@app.route(rule='/up', methods=['GET'])
def up():
    pack = struct.pack('<3i', 0x21010102, updown_val, 0)
    controller.send(pack)
    return 'dog up'


@app.route(rule='/down', methods=['GET'])
def down():
    pack = struct.pack('<3i', 0x21010102, -updown_val, 0)
    controller.send(pack)
    return 'dog down'


@app.route(rule='/stop_ud', methods=['GET'])
def stop_ud():
    pack = struct.pack('<3i', 0x21010102, 0, 0)
    controller.send(pack)
    return 'dog stop up'


# ----------------------------------------------------------------------------------------
#   模式切换
@app.route(rule='/stop_heart', methods=['GET'])
def stop_heart():
    global stop_heartbeat
    if stop_heartbeat:
        stop_heartbeat = False
    else:
        stop_heartbeat = True
    print('dog heart_stop')
    return 'dog heart_stop'


# -------------------------
# 楼梯姿态
@app.route(rule='/ladder', methods=['GET'])
def change_to_ladder():
    pack = struct.pack('<3i', 0x21010401, 0, 0)
    controller.send(pack)
    return 'dog change to ladder'


# 行走姿态
@app.route(rule='/walk', methods=['GET'])
def change_to_walk():
    pack = struct.pack('<3i', 0x21010300, 0, 0)
    controller.send(pack)
    return 'dog change to walk'


# 跑步姿态
@app.route(rule='/run', methods=['GET'])
def change_to_run():
    pack = struct.pack('<3i', 0, 0, 0)
    controller.send(pack)
    return 'doge change to run'


# 站立模式
@app.route(rule='/stand', methods=['GET'])
def change_to_stand():
    global stand
    if stand:
        stand = False
        pack = struct.pack('<3i', 0x21010D06, 0, 0)
        controller.send(pack)
        return 'doge change to move'

    else:
        stand = True
        pack = struct.pack('<3i', 0x21010D05, 0, 0)
        controller.send(pack)
        return 'doge change to stand'


@app.route(rule='/clear', methods=['GET'])
def clear():
    pack = struct.pack('<3i', 0x21010C05, 0, 0)
    controller.send(pack)
    return 'dog clear'


# POST相关的请求
@app.route(rule='/audio', methods=['POST'])
def audio():
    """
        传入的数据格式为json格式
        'way': dz,dxl
        'area': red/yellow/blue
        'people‘：0-6
        ’signal‘：fire,fall
    """
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        if data:
            way = data.get('way')
            if way == 'dz':
                area = data.get('area')
                left_right = data.get('left_right')
                a.dz(area, left_right)
                return 'dog dz audio'
            if way == 'dxl':
                area = data.get('area')
                signal = data.get('signal')
                people = data.get('people')
                a.dxl(area=area, signal=signal, people=people)
                return 'dog dxl audio'
        return 'error: dog not audio'


@app.route('/qr', methods=['GET'])
def qr():
    cap = None
    try:
        cap = cv2.VideoCapture(5)
        for i in range(20):
            ret, frame = cap.read()
            if ret == True:
                res = q.go(frame)
                if res:
                    return res
        return 'error: not find qr code'
    except Exception as e:
        return 'error: no cap'
    finally:
        if cap is not None:
            cap.release()


# ----------------------------------------------------------------------------------------
# 发送一张
def capture_frame():
    t1 = time.time()
    camera = cv2.VideoCapture(5)
    success, frame = camera.read()
    # 使用完要及时释放
    camera.release()
    if success:
        # 外接摄像头比较好的裁剪尺寸
        # 定义裁剪区域的坐标
        x1, y1 = 400, 200
        x2, y2 = 1600, 1300
        # 裁剪图像
        frame = frame[y1:y2, x1:x2]
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        t2 = time.time()
        print(t2-t1)
        # 总耗时 2.2
        return frame


@app.route(rule='/send_img', methods=['GET'])
def send_img():
    return Response(capture_frame(), mimetype='image/jpeg')


# -----------------------------------------------------------------------------------------


# 改变摄像头
@app.route(rule='/change_cap', methods=['GET'])
def change_cap():
    return 'dog cap changed'


# 生成视频流
def generate_frames():
    cap = None
    try:
        cap = cv2.VideoCapture(4)
        while True:
            # 读取视频帧
            success, frame = cap.read()
            if not success:
                break
            else:
                # 在这里可以对视频帧进行处理，例如添加滤镜、人脸识别等
                frame = BlackFindGrayDIY.keep_black(image=frame)
                # # 黑色楼梯
                frame = black_stair.put_text_ratio(frame)

                # frame = WhiteFindGreyDIY.keep_white(image=frame)

                # 白线
                # frame = white_90.put_text_ratio(frame,'right')

                # 深度学习数据采集
                # h, w = 0.8, 0.0
                # # 统计左下角区域的黑色像素数量
                # height, width, _ = frame.shape
                # frame = frame[int(h * height):height, int(w * width):width]


                params = [cv2.IMWRITE_JPEG_QUALITY, 50]  # 质量设置为50
                # 将处理后的视频帧转换为字节流
                ret, buffer = cv2.imencode('.jpg', frame, params)
                frame_bytes = buffer.tobytes()

                # 以字节流的形式发送视频帧
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        print('error')
    finally:
        if cap is not None:
            cap.release()


# -------------------------------------------------
@app.route(rule='/')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# 拓展功能1
# 机器狗识别线左转

def detect_ball(frame):
    # 定义 HSV 范围，用于检测球（橘黄色）
    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([15, 255, 255])

    # 定义 HSV 范围，用于排除草坪（绿色）
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # 将图像转换为 HSV 格式
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 使用 HSV 范围过滤图像中的橘黄色（球）
    mask_ball = cv2.inRange(hsv, lower_orange, upper_orange)

    # 使用 HSV 范围过滤图像中的绿色（草坪）
    mask_grass = cv2.inRange(hsv, lower_green, upper_green)

    # 对球的颜色进行腐蚀和膨胀处理，以消除噪音
    mask_ball = cv2.erode(mask_ball, None, iterations=2)
    mask_ball = cv2.dilate(mask_ball, None, iterations=2)

    # 对草坪的颜色进行腐蚀和膨胀处理，以消除噪音
    mask_grass = cv2.erode(mask_grass, None, iterations=2)
    mask_grass = cv2.dilate(mask_grass, None, iterations=2)

    # 排除草坪的区域
    mask = cv2.bitwise_and(mask_ball, cv2.bitwise_not(mask_grass))

    # 寻找球的轮廓
    contours, _ = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    # 如果没有找到轮廓，返回 None
    if len(contours) == 0:
        return None, None

    # 找到最大的轮廓
    max_contour = max(contours, key=cv2.contourArea)

    # 计算最小外接圆
    ((x, y), radius) = cv2.minEnclosingCircle(max_contour)

    # 如果半径大于设定阈值，则认为检测到了球
    if radius > 10:
        return (int(x), int(y)), int(radius)
    else:
        return None, None

# 无敌的踢球
def auto_ball():
    # 打开摄像头
    cap = cv2.VideoCapture(4)

    # 设置图像中心位置(后续修改为狗可以提到球的中心位置)
    image_center_x = 650
    image_center_y = 100

    # 设置宽泛的偏移范围
    offset_threshold = 25

    # 是否已经前进过的标志位
    forwarded = False
    c = 0
    lr = 0
    while True:
        c += 1
        print('c',c)
        # 读取一帧
        ret, frame = cap.read()
        # 如果成功读取帧
        if ret:
            if c >= 30:
                # 检测球
                ball_position, ball_radius = detect_ball(frame)
                print('检测ball')
                if ball_position is None:
                    print('没有小球')
                    time.sleep(0.2)
                    controller.send(struct.pack('<3i', 0x21010130, 0, 0))
                    break
                if ball_position is not None:
                    # 从 detect_ball 函数返回的结果中提取球的位置和半径
                    (ball_x, ball_y) = ball_position
                    # 在图像中标记球的位置
                    # cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 255, 0), 2)
                    # cv2.putText(frame, 'Ball', (ball_x, ball_y),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

                    # 无敌的版本，计算斜率版本，越远，越精准
                    offset_x = 670 - ball_x + (1080 - ball_y) / 5.15 -offset_threshold

                    # hong的踢球,配合转圈使用
                    # offset_x = ball_x - image_center_x

                    # 后续可能使用来优化:判断是否踢到到了球
                    # offset_y = ball_y - image_center_y

                    if lr == 0:
                        # 如果偏移量在一定范围内，左移或右移
                        if abs(offset_x) > offset_threshold:
                            if offset_x > 0:
                                # 左移
                                controller.send(struct.pack('<3i', 0x21010131, -20000, 0))
                            else:
                                # 右移动
                                controller.send(struct.pack('<3i', 0x21010131, 20000, 0))
                        else:
                            # 在一定范围内，前进一次
                            controller.send(struct.pack('<3i', 0x21010131, 0, 0))
                            lr = 1

                    if lr == 1:
                        controller.send(struct.pack('<3i', 0x21010130, 22000, 0))
        if c > 400:
            controller.send(struct.pack('<3i', 0x21010131, 0, 0))
            time.sleep(0.1)
            controller.send(struct.pack('<3i', 0x21010130, 0, 0))
            break

# AutoBall
@app.route(rule='/auto_ball')
def dog_auto_ball():
    auto_ball()
    # pack = struct.pack('<3i', 0x21010135, 13000, 0)
    # controller.send(pack)
    # time.sleep(3)
    # pack = struct.pack('<3i', 0x21010135, 0, 0)
    # controller.send(pack)
    return 'dog auto ball '

# 1.05 移动旋转
# 1.35 停止旋转
@app.route(rule='/1')
def more_1():
    print('start 1')
    cap = None
    try:
        cap = cv2.VideoCapture(cap_number)
        c = 0
        pack = struct.pack('<3i', 0x21010130, auto_fb_val, 0)
        controller.send(pack)
        while True:
            c += 1
            if c > 4:
                # 读取视频帧
                success, frame = cap.read()
                if not success:
                    break
                else:
                    # 二值化
                    frame = WhiteFindGreyDIY.keep_white(frame)

                    is_turn_left = white_90.is_turn_left(frame)
                    if is_turn_left:
                        # 停止前进
                        time.sleep(0.5)
                        pack = struct.pack('<3i', 0x21010130, 0, 0)
                        controller.send(pack)
                        time.sleep(3)

                        # 左转
                        pack = struct.pack('<3i', 0x21010135, -13000, 0)
                        controller.send(pack)
                        time.sleep(1.35)
                        pack = struct.pack('<3i', 0x21010135, 0, 0)
                        controller.send(pack)
                        return 'turn_left_90'

                if c > 400:
                    pack = struct.pack('<3i', 0x21010130, 0, 0)
                    controller.send(pack)
                    return '1 over'
    except Exception as e:
        print('error')
        pack = struct.pack('<3i', 0x21010130, 0, 0)
        controller.send(pack)
        return 'err auto_turn_left:'
    finally:
        if cap is not None:
            cap.release()


# 机器狗识别线右转
@app.route(rule='/2')
def more_2():
    print('start 2')
    cap = None
    try:
        cap = cv2.VideoCapture(cap_number)
        c = 0
        pack = struct.pack('<3i', 0x21010130, auto_fb_val, 0)
        controller.send(pack)
        while True:
            c += 1
            # 读取视频帧
            success, frame = cap.read()
            if not success:
                break
            else:
                if c > 8:
                    # 二值化
                    frame = WhiteFindGreyDIY.keep_white(frame)

                    is_turn_right = white_90.is_turn_right(frame)
                    if is_turn_right:
                        # 停止前进
                        time.sleep(1)
                        pack = struct.pack('<3i', 0x21010130, 0, 0)
                        controller.send(pack)
                        time.sleep(3)

                        # 右转
                        pack = struct.pack('<3i', 0x21010135, 13000, 0)
                        controller.send(pack)
                        time.sleep(1.35)
                        pack = struct.pack('<3i', 0x21010135, 0, 0)
                        controller.send(pack)
                        return 'turn_right_90'

                if c > 400:
                    pack = struct.pack('<3i', 0x21010130, 0, 0)
                    controller.send(pack)
                    return '2 over'
    except Exception as e:
        print('error')
        pack = struct.pack('<3i', 0x21010130, 0, 0)
        controller.send(pack)
        return 'err auto_turn_right:'
    finally:
        if cap is not None:
            cap.release()


# 楼梯步过楼梯
@app.route(rule='/3')
def more_3():
    print('start 3')
    cap = None
    try:
        cap = cv2.VideoCapture(cap_number)
        c = 0
        # 前进
        pack = struct.pack('<3i', 0x21010130, auto_fb_val, 0)
        controller.send(pack)
        while True:
            c += 1
            # 读取视频帧
            success, frame = cap.read()
            if not success:
                break
            else:
                if c > 8:
                    # 二值化
                    frame = BlackFindGrayDIY.keep_black(frame)

                    is_stair_step = black_stair.is_stair_step(frame)
                    if is_stair_step:
                        # 停止前进
                        pack = struct.pack('<3i', 0x21010130, 0, 0)
                        controller.send(pack)
                        time.sleep(1)

                        # 切换为楼梯步
                        pack = struct.pack('<3i', 0x21010401, 0, 0)
                        controller.send(pack)
                        # 前进过楼梯
                        pack = struct.pack('<3i', 0x21010130, fb_val, 0)
                        controller.send(pack)
                        time.sleep(3.5)
                        pack = struct.pack('<3i', 0x21010130, 0, 0)
                        controller.send(pack)

                        # 切换为行走态
                        pack = struct.pack('<3i', 0x21010300, 0, 0)
                        controller.send(pack)
                        return 'stair_step'

                if c > 400:
                    pack = struct.pack('<3i', 0x21010130, 0, 0)
                    controller.send(pack)
                    return '3 over'

    except Exception as e:
        print('error')
    finally:
        if cap is not None:
            cap.release()


# step_1 左转90度
@app.route(rule='/4')
def more_4():
    print('start 4')
    cap = None
    try:
        cap = cv2.VideoCapture(cap_number)
        c = 0
        while True:
            c += 1
            if c == 4:
                pack = struct.pack('<3i', 0x21010130, auto_fb_val, 0)
                controller.send(pack)
            if c > 4:
                # 读取视频帧
                success, frame = cap.read()
                if not success:
                    break
                else:
                    # 二值化
                    frame = WhiteFindGreyDIY.keep_white(frame)

                    is_turn_left = white_90.is_turn_left(frame)
                    if is_turn_left:
                        # 停止前进
                        time.sleep(1.5)
                        pack = struct.pack('<3i', 0x21010130, 0, 0)
                        controller.send(pack)
                        time.sleep(3)

                        # 左转
                        pack = struct.pack('<3i', 0x21010135, -13000, 0)
                        controller.send(pack)
                        time.sleep(1.35)
                        pack = struct.pack('<3i', 0x21010135, 0, 0)
                        controller.send(pack)
                        return 'turn_left_90'

                if c > 400:
                    pack = struct.pack('<3i', 0x21010130, 0, 0)
                    controller.send(pack)
                    return '1 over'
    except Exception as e:
        print('error')
        pack = struct.pack('<3i', 0x21010130, 0, 0)
        controller.send(pack)
        return 'err auto_turn_left:'
    finally:
        if cap is not None:
            cap.release()


# step_2 右转90度
@app.route(rule='/5')
def more_5():
    print('start 5')
    cap = None
    try:
        cap = cv2.VideoCapture(cap_number)
        c = 0
        while True:
            c += 1
            if c == 4:
                pack = struct.pack('<3i', 0x21010130, auto_fb_val, 0)
                controller.send(pack)
            # 读取视频帧
            success, frame = cap.read()
            if not success:
                break
            else:
                if c > 4:
                    # 二值化
                    frame = WhiteFindGreyDIY.keep_white(frame)

                    is_turn_right = white_90.is_turn_right(frame)
                    if is_turn_right:
                        # 停止前进
                        time.sleep(1.5)
                        pack = struct.pack('<3i', 0x21010130, 0, 0)
                        controller.send(pack)
                        time.sleep(3)

                        # 右转
                        pack = struct.pack('<3i', 0x21010135, 13000, 0)
                        controller.send(pack)
                        time.sleep(1.35)
                        pack = struct.pack('<3i', 0x21010135, 0, 0)
                        controller.send(pack)
                        return 'turn_right_90'

                if c > 400:
                    pack = struct.pack('<3i', 0x21010130, 0, 0)
                    controller.send(pack)
                    return '2 over'
    except Exception as e:
        print('error')
        pack = struct.pack('<3i', 0x21010130, 0, 0)
        controller.send(pack)
        return 'err auto_turn_right:'
    finally:
        if cap is not None:
            cap.release()

# 第三个楼梯左拐
@app.route(rule='/6')
def more_6():
    print('start 1')
    cap = None
    try:
        cap = cv2.VideoCapture(cap_number)
        c = 0
        pack = struct.pack('<3i', 0x21010130, auto_fb_val, 0)
        controller.send(pack)
        while True:
            c += 1
            if c > 4:
                # 读取视频帧
                success, frame = cap.read()
                if not success:
                    break
                else:
                    # 二值化
                    frame = WhiteFindGreyDIY.keep_white(frame)

                    is_turn_left = white_90.is_turn_left(frame)
                    if is_turn_left:
                        # 停止前进
                        time.sleep(1.25)
                        pack = struct.pack('<3i', 0x21010130, 0, 0)
                        controller.send(pack)
                        time.sleep(3)

                        # 左转
                        pack = struct.pack('<3i', 0x21010135, -13000, 0)
                        controller.send(pack)
                        time.sleep(1.35)
                        pack = struct.pack('<3i', 0x21010135, 0, 0)
                        controller.send(pack)
                        return 'turn_left_90'

                if c > 400:
                    pack = struct.pack('<3i', 0x21010130, 0, 0)
                    controller.send(pack)
                    return '1 over'
    except Exception as e:
        print('error')
        pack = struct.pack('<3i', 0x21010130, 0, 0)
        controller.send(pack)
        return 'err auto_turn_left:'
    finally:
        if cap is not None:
            cap.release()

# 前往足球区域
@app.route(rule='/0')
def more_0():
    print('start 0')
    cap = None
    try:
        cap = cv2.VideoCapture(cap_number)
        c = 0
        pack = struct.pack('<3i', 0x21010130, fb_val, 0)
        controller.send(pack)
        time.sleep(4)
        while True:
            c += 1
            # 读取视频帧
            success, frame = cap.read()
            if not success:
                break
            else:
                # 二值化
                frame = WhiteFindGreyDIY.keep_white(frame)

                is_turn_left = white_90.is_turn_right(frame)
                if is_turn_left:
                    # 停止前进
                    time.sleep(0.3)
                    pack = struct.pack('<3i', 0x21010130, 0, 0)
                    controller.send(pack)
                    time.sleep(1)
                    return 'forward to ball'

                if c > 400:
                    pack = struct.pack('<3i', 0x21010130, 0, 0)
                    controller.send(pack)
                    return '4 over'
    except Exception as e:
        print('error')
    finally:
        if cap is not None:
            cap.release()

# 运行应用程序
if __name__ == '__main__':
    heart_exchange_thread.daemon = True
    heart_exchange_thread.start()
    app.run(host='0.0.0.0', debug=True, port=5000)
