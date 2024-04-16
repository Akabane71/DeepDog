import time

import cv2
import requests
import numpy as np

t1 = time.time()
# 发送GET请求获取图像数据
response = requests.get('http://192.168.1.101:5000/send_img')

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
