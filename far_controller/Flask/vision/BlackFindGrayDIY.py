'''
使用灰度处理将视频中的黑色突出显示
便于后续处理识别黑色台阶
其中RGB自定义权重红色排除影响
'''

import cv2
from PIL import Image
import numpy as np

# 比赛的方案
def keep_black(image, r_weight=0, g_weight=0.7, b_weight=0.3):
    # 将图像转换为灰度图
    gray = r_weight * image[:, :, 2] + g_weight * \
           image[:, :, 1] + b_weight * image[:, :, 0]

    # 将灰度图转换为二值图像，阈值设为 50
    _, binary = cv2.threshold(gray.astype('uint8'), 50, 255, cv2.THRESH_BINARY)

    # 算法有一些零碎的黑色区域，需要用算法去噪
    """
        去噪算法  or  自适应二值化
    """
    binary = dilated_img(binary)
    return binary


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

# 对图像进行膨胀
def dilated_img(img):
    # 定义膨胀核（这里使用一个3x3的正方形核）
    kernel = np.ones((3, 3), np.uint8)

    # 对图像进行膨胀操作
    dilated_img = cv2.dilate(img, kernel, iterations=1)
    return dilated_img


# 寻找黑色轮廓并将轮廓和中心标出
def find_black_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    # 轮廓检测
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到面积最大的轮廓
    max_contour = max(contours, key=cv2.contourArea)

    # 计算轮廓的面积
    area = cv2.contourArea(max_contour)

    # 如果轮廓面积超过阈值，则绘制轮廓和中点
    min_area_threshold = 1000  # 轮廓最小面积阈值
    if area > min_area_threshold:
        # 绘制轮廓
        cv2.drawContours(image, [max_contour], -1, (0, 0, 255), 2)

        # 计算轮廓中心
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # 在轮廓中心绘制绿色点
            cv2.circle(image, (cX, cY), 5, (0, 255, 0), -1)

    return image


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
