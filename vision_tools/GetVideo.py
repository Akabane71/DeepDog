import imageio  # RGB 需要手动安装
import numpy as np
import cv2 # BGR

def record_video(filename, frame_width=640, frame_height=480, duration=20):
    # 创建视频编码器
    writer = imageio.get_writer(filename, fps=16*2)

    # 打开摄像头
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # 录制视频
    start_time = cv2.getTickCount()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 将帧添加到视频
        writer.append_data(frame_rgb)

        # 显示实时预览
        cv2.imshow("Recording", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 检查录制时间是否达到指定时长
        current_time = cv2.getTickCount()
        elapsed_time = (current_time - start_time) / cv2.getTickFrequency()
        if elapsed_time >= duration:
            break

    # 关闭摄像头和视频编码器
    cap.release()
    writer.close()

if __name__ == "__main__":
    filename = "recorded_video.mp4"  # 视频文件名
    frame_width = 640  # 视频帧宽度
    frame_height = 480  # 视频帧高度
    duration = 10  # 录制时长（秒）

    record_video(filename, frame_width, frame_height, duration)
