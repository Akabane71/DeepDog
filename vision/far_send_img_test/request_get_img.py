import time

import cv2
import requests
import numpy as np

"""
    研究结论，摄像头的打开与关闭占用了大量的资源，消耗了大量的时间，是阻塞操作，
    建议将摄像头作为全局变量资源，进行定义
    
    : 先定义---> 0.2s
    : 定义再销毁: ---> 1.19s
"""



t1 = time.time()
# 发送GET请求获取图像数据
response = requests.get('http://192.168.1.105:5000/')

# 将获取的图像数据转换为numpy数组
arr = np.frombuffer(response.content, np.uint8)

# 将numpy数组解码为图像
img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
t2 = time.time()
# 耗时越2s
print(t2-t1)
# 显示图像
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
