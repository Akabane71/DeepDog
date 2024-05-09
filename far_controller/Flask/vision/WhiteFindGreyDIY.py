'''
使用灰度处理将将视频中白色突出显示
便于后续处理识别白线
其中RGB自定义权重红色排除影响
'''

import cv2


def keep_white(image, r_weight=0, g_weight=0.5, b_weight=0.5):
    # 将图像转换为灰度图
    gray = r_weight * image[:, :, 2] + g_weight * \
        image[:, :, 1] + b_weight * image[:, :, 0]

    # 将灰度图转换为二值图像，阈值设为 200（适应白色的颜色范围）
    _, binary = cv2.threshold(gray.astype(
        'uint8'), 200, 255, cv2.THRESH_BINARY)

    result = binary

    return result






if __name__ == "__main__":
    # 摄像头捕获
    cap = cv2.VideoCapture(0)

    while True:
        # 从摄像头捕获一帧
        ret, frame = cap.read()
        if not ret:
            break

        # 处理图像，默认权重为红色最低，绿色次之，蓝色最高
        processed_img = keep_white(frame)

        # 显示图像
        cv2.imshow('Processed Image', processed_img)

        # 按下 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
