import pyrealsense2 as rs
import numpy as np
import cv2

# 配置深度摄像机
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 开始深度流
pipeline.start(config)

try:
    while True:
        # 等待深度图像
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # 将深度图像转换为Numpy数组
        depth_image = np.asanyarray(depth_frame.get_data())

        # 将彩色图像转换为OpenCV格式
        color_image = np.asanyarray(color_frame.get_data())

        # 在窗口中显示深度图像
        cv2.imshow('Depth Image', depth_image)
        cv2.imshow('Color Image', color_image)

        # 按下 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 关闭流，释放资源
    pipeline.stop()
    cv2.destroyAllWindows()
