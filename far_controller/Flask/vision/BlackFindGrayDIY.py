'''
使用灰度处理将视频中的黑色突出显示
便于后续处理识别黑色台阶
其中RGB自定义权重红色排除影响
'''

import cv2
from PIL import Image
import numpy as np


def keep_black(image, r_weight=0, g_weight=0.7, b_weight=0.3):
    # 将图像转换为灰度图
    gray = r_weight * image[:, :, 2] + g_weight * \
           image[:, :, 1] + b_weight * image[:, :, 0]

    # 将灰度图转换为二值图像，阈值设为 50
    _, binary = cv2.threshold(gray.astype('uint8'), 50, 255, cv2.THRESH_BINARY)

    return binary


# 比赛方案
def dev_green(frame):
    # 将帧转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定义绿色范围
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # 创建一个掩码，将绿色区域提取出来
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # 将绿色区域替换为白色
    frame[mask > 0] = [255, 255, 255]

    # 将黑色区域替换为黑色
    frame[mask == 0] = [0, 0, 0]

    # 将图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 对灰度图进行二值化
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    return binary


if __name__ == "__main__":
    # 摄像头捕获
    cap = cv2.VideoCapture(0)

    while True:
        # 从摄像头捕获一帧
        ret, frame = cap.read()
        if not ret:
            break

        # 处理图像，默认权重为红色最低，绿色次之，蓝色最高
        processed_img = keep_black(frame)

        # 显示图像
        cv2.imshow('Processed Image', processed_img)

        # 按下 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
