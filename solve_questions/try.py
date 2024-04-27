import cv2
import numpy as np



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


# 打开摄像头
cap = cv2.VideoCapture(4)

# 设置图像中心位置(后续修改为狗可以提到球的中心位置)
image_center_x = 960
image_center_y = 100

# 设置宽泛的偏移范围
offset_threshold = 100

# 是否已经前进过的标志位
forwarded = False
sit = 0
x = 0
y = 0
while True:
    # 读取一帧
    ret, frame = cap.read()

    # 如果成功读取帧
    if ret:
        # 检测球
        ball_position, ball_radius = detect_ball(frame)

        if ball_position is not None:
            # 从 detect_ball 函数返回的结果中提取球的位置和半径
            (ball_x, ball_y) = ball_position
            if (sit == 0):
                x = ball_x
                y = ball_y
                sit = 1
            if (abs(x) - abs(ball_x) > 400):
                break
            # 在图像中标记球的位置
            cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 255, 0), 2)
            cv2.putText(frame, 'Ball', (ball_x, ball_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

            # 计算球距离图像中心的偏移量
            offset_x = ball_x - image_center_x
            # 后续可能使用来优化:判断是否踢到到了球
            # offset_y = ball_y - image_center_y

            # 如果偏移量在一定范围内，左移或右移
            if abs(offset_x) > offset_threshold:
                if offset_x < 0:
                    left()
                else:
                    right()
            else:
                # 在一定范围内，前进一次
                if not forwarded:
                    go_forward()
            if(point==2):
                break
        # 显示结果
        cv2.imshow('Ball Detection', frame)

        # 主动结束：按下 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('m'):
            break
