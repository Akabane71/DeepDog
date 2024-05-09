import cv2
import requests
from threading import Thread
import numpy as np


def go(w):
    pass

def process_frame(frame):
    # 获取图像的高度和宽度
    image_height, image_width, _ = frame.shape

    # 转换颜色空间为HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定义橙色范围的阈值
    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([15, 255, 255])

    # 创建橙色掩膜
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # 执行形态学操作，去除噪音
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # 寻找橙色小球的轮廓
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 初始化小球位置
    ball_position = None

    if len(contours) >= 1:
        # 找到最大的轮廓（橙色小球）
        max_contour = max(contours, key=cv2.contourArea)

        # 计算最大轮廓的外接圆
        ((x, y), radius) = cv2.minEnclosingCircle(max_contour)

        # 计算小球在图像中的中心位置
        ball_position = (int(x), int(y))

        # 绘制圆圈和中心点
        cv2.circle(frame, ball_position, int(radius), (0, 255, 255), 2)
        cv2.circle(frame, ball_position, 5, (0, 0, 255), -1)
        return frame, ball_position


def auto_ball_forward(cap):
    while True:
        # 读取帧
        ret, frame = cap.read()
        if frame is not None:
            print('ok')
            # 图片裁剪
            # frame = frame[720:1080, 0:1920]
        if not ret:
            return '摄像头调用失败'
        # 处理后的图像  # 中心位置
        frame, ball_position = process_frame(frame)
        if ball_position is not None:
            print('前进')
        # 显示图像
        cv2.imshow("Orange Ball Tracking", frame)

        # 退出循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 释放摄像机并关闭窗口
    cap.release()
    cv2.destroyAllWindows()
    print('成功完成踢球')


if __name__ == '__main__':
    try:
        cap = cv2.VideoCapture(0)
        auto_ball_forward(cap)
    except Exception as e:
        print('黄色小球超出视野')