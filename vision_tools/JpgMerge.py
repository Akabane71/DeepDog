import os
import shutil

"""
    将多个文件夹下的图片移动到指定文件夹下并将重复文件重新命名
"""

def merge_images(source_dirs, destination_dir):
    # 创建目标目录
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 遍历源目录
    for source_dir in source_dirs:
        # 获取源目录下的所有文件
        files = os.listdir(source_dir)

        # 遍历文件
        for file in files:
            # 检查文件是否为图片
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                source_path = os.path.join(source_dir, file)
                # 生成目标文件名
                dest_filename = file
                dest_path = os.path.join(destination_dir, dest_filename)

                # 如果文件已存在，则重命名
                index = 1
                while os.path.exists(dest_path):
                    # 重新命名文件
                    filename, extension = os.path.splitext(file)
                    dest_filename = f"{filename}_{index}{extension}"
                    dest_path = os.path.join(destination_dir, dest_filename)
                    index += 1

                # 复制文件到目标目录
                shutil.copy2(source_path, dest_path)


if __name__ == "__main__":
    # 指定源目录列表
    source_dirs = ["imgs/01", "imgs/02","imgs/03","imgs/04","imgs/05"]  # 修改为实际的源目录列表

    # 指定目标目录
    destination_dir = "imgs/total"  # 修改为实际的目标目录

    # 执行合并操作
    merge_images(source_dirs, destination_dir)
