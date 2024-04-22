import requests
import cv2
import numpy as np

# 定义视频流的 URL
video_url = 'http://192.168.1.101:5000/'

# 发送 GET 请求获取视频流
response = requests.get(video_url, stream=True)

# 如果请求成功
if response.status_code == 200:
    # 打开一个视频文件用于存储接收到的数据
    out = cv2.VideoWriter('received_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))

    # 循环读取视频流
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            # 将字节流转换为图像数据
            nparr = np.frombuffer(chunk, dtype=np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 在这里可以对接收到的视频帧进行处理，例如保存到视频文件中
            out.write(frame)

    # 关闭视频文件
    out.release()
    print("Video stream saved as 'received_video.mp4'.")
else:
    print("Failed to receive video stream.")
