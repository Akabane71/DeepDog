import cv2
import numpy as np
import os

"""
    从网络视频流直接获取数据,并抽帧存储到本地
"""

def decode_video_stream(url):
    try:
        # 打开网络视频流
        cap = cv2.VideoCapture(url)

        # 检查视频流是否成功打开
        if not cap.isOpened():
            print("Error: Unable to open video stream.")
            return

        # 循环读取并显示视频帧
        while True:
            ret, frame = cap.read()

            # 检查帧是否成功读取
            if not ret:
                print("Error: Unable to read frame.")
                break

            # 在这里可以对帧进行处理，例如显示、保存等
            cv2.imshow('Frame', frame)

            # 按下'q'键退出循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 释放视频流资源
        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print('Error:', e)

def main_show_video():
    # 要解码的网络视频流URL
    video_url = 'http://192.168.1.105:5000'

    # 调用函数解码视频流
    decode_video_stream(video_url)


def get_img_from_net(url,folder_path):
    # 创建文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    try:
        # 打开网络视频流
        cap = cv2.VideoCapture(url)

        # 检查视频流是否成功打开
        if not cap.isOpened():
            print("Error: Unable to open video stream.")
            return

        # 循环读取并显示视频帧
        while True:
            ret, frame = cap.read()

            # 检查帧是否成功读取
            if not ret:
                print("Error: Unable to read frame.")
                break
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

                if c % 3 == 0:
                    # 构造保存路径
                    filename = os.path.join(folder_path, f"frame_{a}.jpg")

                    # 将当前帧保存到指定文件夹
                    cv2.imwrite(filename, frame)
                    a += 1
                    # 显示当前帧
                    cv2.imshow('Frame', frame)
                c += 1
                # 按下'q'键退出循环
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # 释放视频流资源
        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print('Error:', e)

def main_download_img():
    url = 'http://192.168.1.101:5000/'
    folder_path = '../data/dataset'
    get_img_from_net(url, folder_path)


if __name__ == '__main__':
    main_download_img()

