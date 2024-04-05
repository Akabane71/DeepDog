import cv2
import os

def extract_frames(video_path, output_folder, interval=0.1):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 确保视频文件能够打开
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    while True:
        # 读取视频的一帧
        ret, frame = cap.read()

        if not ret:
            break

        # 计算帧的编号
        frame_count += 1

        # 每隔指定时间间隔保存一帧
        if frame_count % int(cap.get(cv2.CAP_PROP_FPS) * interval) == 0:
            # 构造输出文件名
            output_filename = os.path.join(output_folder, f"{frame_count}.jpg")

            # 保存帧为图片
            cv2.imwrite(output_filename, frame)

    # 关闭视频文件
    cap.release()

if __name__ == "__main__":
    video_path = "./videos/recorded_video.mp4"  # 视频文件路径
    output_folder = "./imgs"  # 输出文件夹路径
    interval = 0.2  # 保存帧的时间间隔（秒）

    extract_frames(video_path, output_folder, interval)
