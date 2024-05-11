import cv2

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 读取第一帧
ret, frame = cap.read()

# 获取图像尺寸
height, width, _ = frame.shape
print("图像宽度:", width)
print("图像高度:", height)

# 关闭摄像头
cap.release()
