import cv2
import os

"""
    打开摄像头按下space截图，存储到本地
"""
def capture_and_save_frames(output_directory, target_size=(512, 512)):
    # 创建输出目录
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 初始化文件计数器
    file_count = 0

    while True:
        # 读取当前帧
        ret, frame = cap.read()

        # 如果成功读取帧
        if ret:
            # 调整图像大小为目标尺寸
            frame = cv2.resize(frame, target_size)

            # 检测按键
            key = cv2.waitKey(1)

            # 如果按下空格键 (32对应空格键的ASCII码)
            if key == 32:
                # 递增文件计数器
                file_count += 1

                # 构造文件名
                file_name = f"{file_count}.jpg"

                # 构造完整的输出路径
                output_path = os.path.join(output_directory, file_name)

                # 保存帧到文件
                cv2.imwrite(output_path, frame)

                print(f"Saved {file_name}")

            # 按下 'q' 键退出循环
            elif key == ord('q'):
                break
        cv2.imshow('frame',frame)

    # 释放摄像头资源
    cap.release()

    # 关闭所有窗口
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # 指定输出目录
    output_directory = ("./imgs")

    # 调用函数进行捕获和保存帧
    capture_and_save_frames(output_directory)
