import cv2
import time
import struct
import numpy as np

# 获取黄色三角形
def get_yellow_re(frame):
    # 转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用Canny算子进行边缘检测
    edges = cv2.Canny(gray, 100, 200)  # 调整阈值参数以适应你的图像

    # 查找边缘图像中的轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 初始化最大面积和最大轮廓
    max_area = 0
    max_contour = None

    for contour in contours:
        # 近似轮廓
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # 如果近似轮廓有三个顶点，说明是三角形
        if len(approx) == 3:
            # 计算轮廓的面积
            area = cv2.contourArea(contour)

            # 如果面积大于最大面积，更新最大面积和最大轮廓
            if area > max_area:
                max_area = area
                max_contour = contour

    # 在屏幕中央绘制紫色竖线
    screen_center = (frame.shape[1] // 2, frame.shape[0] // 2)
    cv2.line(frame, screen_center, screen_center, (128, 0, 128), 3)

    # 如果找到了最大轮廓，绘制其轮廓并计算内心
    if max_contour is not None:
        cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)

        # 计算最大轮廓的内心
        M = cv2.moments(max_contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # 在图像上绘制内心点
        cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
        about = 10

        # 判断内心与竖线的位置关系
        if cX + about < screen_center[0]:
            cv2.putText(frame, "Triangle center is on the left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
            print('left')
        elif cX - about > screen_center[0]:
            cv2.putText(frame, "Triangle center is on the right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
            print('right')
        else:
            cv2.putText(frame, "Triangle center is at the center", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
    # 返回图片
    return frame

def re_site():
    last = 0
    # 初始化摄像头
    cap = cv2.VideoCapture(5)  # 0 表示默认摄像机
    need = 0
    while True:
        need += 2
        # 读取帧
        ret, frame = cap.read()
        # frame = frame[650:1080, 410:1510]

        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 使用Canny算子进行边缘检测
        edges = cv2.Canny(gray, 100, 200)  # 调整阈值参数以适应你的图像

        # 查找边缘图像中的轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 初始化最大面积和最大轮廓
        max_area = 0
        max_contour = None

        for contour in contours:
            # 近似轮廓
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # 如果近似轮廓有三个顶点，说明是三角形
            if len(approx) == 3:
                # 计算轮廓的面积
                area = cv2.contourArea(contour)

                # 如果面积大于最大面积，更新最大面积和最大轮廓
                if area > max_area:
                    max_area = area
                    max_contour = contour

        # 在屏幕中央绘制紫色竖线
        screen_center = (frame.shape[1] // 2, frame.shape[0] // 2)
        cv2.line(frame, screen_center, screen_center, (128, 0, 128), 2)

        # 如果找到了最大轮廓，绘制其轮廓并计算内心
        if max_contour is not None:
            cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)

            # 计算最大轮廓的内心
            M = cv2.moments(max_contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # 在图像上绘制内心点
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
            about = 10

            # 判断内心与竖线的位置关系
            if cX + about < screen_center[0]:
                cv2.putText(frame, "Triangle center is on the left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)
                print('left')
            elif cX - about > screen_center[0]:
                cv2.putText(frame, "Triangle center is on the right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)
                print('right')
            else:
                cv2.putText(frame, "Triangle center is at the center", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)

        # 显示图像
        cv2.imshow("Largest Triangle with Canny Edge Detection", frame)

        # 按下'q'键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    re_site()