import cv2

# 视频测试
def put_text_ratio(binary):
    h, w = 0.75, 0.0
    # 统计左下角区域的黑色像素数量
    height, width = binary.shape
    roi = binary[int(h * height):height, int(w * width):width]
    black_pixels = cv2.countNonZero(roi)

    # 计算白色像素所占比例
    total_pixels = roi.shape[0] * roi.shape[1]
    black_pixel_ratio = black_pixels / total_pixels
    black_pixel_ratio = 1 - black_pixel_ratio
    print(black_pixel_ratio)

    # 在图像上打印比例
    text = "black: {:.2f}%".format(black_pixel_ratio * 100)
    cv2.putText(binary, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # 绘制左下角区域的矩形
    cv2.rectangle(binary, (int(w * width), int(h * height)), (width, height), (0, 0, 0), 2)
    return binary

# 楼梯步过楼梯
def is_stair_step(binary):
    h, w = 0.75, 0.0
    # 统计左下角区域的黑色像素数量
    height, width = binary.shape
    roi = binary[int(h * height):height, int(w * width):width]
    black_pixels = cv2.countNonZero(roi)

    # 计算黑色像素所占比例
    total_pixels = roi.shape[0] * roi.shape[1]
    black_pixel_ratio = 1 - (black_pixels / total_pixels)

    print('>',black_pixel_ratio)
    if black_pixel_ratio > 0.200 and black_pixel_ratio < 0.5:
        return True
    else:
        return False



