import cv2
import os

"""
    机器狗图像数据采集,本地采集
"""

def save_frame_to_folder(folder_path):
    # 创建文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    try:
        c = 0
        a = 0
        while True:
            # 读取当前帧
            ret, frame = cap.read()

            # 检查帧是否成功读取
            if not ret:
                print("Error: Unable to read frame.")
                break

            # 在此处进行图像处理或其他操作，如果需要的话

            if c %3 == 0:
                # 构造保存路径
                filename = os.path.join(folder_path, f"frame_{a}.jpg")

                # 将当前帧保存到指定文件夹
                cv2.imwrite(filename, frame)
                a += 1
                # 显示当前帧
                cv2.imshow('Frame', frame)
            c += 1
            # 等待按键事件，按下'q'键退出循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # 释放摄像头资源
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # 指定保存图片的文件夹路径
    folder_path = ("../data")
    save_frame_to_folder(folder_path)
