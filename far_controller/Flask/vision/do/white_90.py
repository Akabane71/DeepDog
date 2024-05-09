import cv2

# 视觉测试工具
def put_text_ratio(binary,left_right):
    if left_right == 'left':
        h, w = 0.9, 0.5
        # 左半边
        # 统计左下角区域的白色像素数量
        height, width = binary.shape
        roi = binary[int(h * height):height, 0:int(w * width)]
        white_pixels = cv2.countNonZero(roi)

        # 计算白色像素所占比例
        total_pixels = roi.shape[0] * roi.shape[1]
        white_pixel_ratio = white_pixels / total_pixels

        # 在图像上打印比例
        text = "white: {:.2f}%".format(white_pixel_ratio * 100)
        cv2.putText(binary, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 绘制左下角区域的矩形
        cv2.rectangle(binary, (0, int(h * height)), (int(w * width), height), (255, 255, 255), 2)
        return binary
    else:
        h, w = 0.9, 0.0
        # 右半边
        # 统计右下角区域的白色像素数量
        height, width = binary.shape
        roi = binary[int(h * height):height, int(w * width):width]
        white_pixels = cv2.countNonZero(roi)

        # 计算白色像素所占比例
        total_pixels = roi.shape[0] * roi.shape[1]
        white_pixel_ratio = white_pixels / total_pixels

        # 在图像上打印比例
        text = "white: {:.2f}%".format(white_pixel_ratio * 100)
        cv2.putText(binary, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 绘制右下角区域的矩形
        cv2.rectangle(binary, (int(w * width), int(h * height)), (width, height), (255, 255, 255), 2)
        return binary


# 左转拐点
def is_turn_left(binary):
    h, w = 0.9, 0.5
    # 统计左下角区域的白色像素数量
    height, width = binary.shape
    roi = binary[int(h * height):height, 0:int(w * width)]
    white_pixels = cv2.countNonZero(roi)

    # 计算白色像素所占比例
    total_pixels = roi.shape[0] * roi.shape[1]
    white_pixel_ratio = white_pixels / total_pixels

    if white_pixel_ratio > 0.3:
        return True
    else:
        return False


# 右转拐点
def is_turn_right(binary):
    h, w = 0.9, 0.0
    # 统计右下角区域的白色像素数量
    height, width = binary.shape
    roi = binary[int(h * height):height, int(w * width):width]
    white_pixels = cv2.countNonZero(roi)

    # 计算白色像素所占比例
    total_pixels = roi.shape[0] * roi.shape[1]
    white_pixel_ratio = (white_pixels / total_pixels)
    # print(white_pixel_ratio)

    # 结束标志
    if white_pixel_ratio > 0.1:
        return True
    else:
        return False
