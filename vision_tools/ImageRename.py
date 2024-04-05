import os

def rename_files(folder_path):
    # 获取文件夹中所有的.jpg文件
    jpg_files = [file for file in os.listdir(folder_path) if file.endswith('.jpg')]

    # 对文件进行排序
    jpg_files.sort()

    # 遍历文件并进行重新命名
    for i, file in enumerate(jpg_files):
        old_path = os.path.join(folder_path, file)
        new_name = f"{i:03d}.jpg"  # 根据索引进行编号，例如000.jpg, 001.jpg, ..., 099.jpg, 100.jpg, ...
        new_path = os.path.join(folder_path, new_name)

        # 重命名文件
        os.rename(old_path, new_path)

if __name__ == "__main__":
    folder_path = "./imgs"  # 图片文件夹路径

    rename_files(folder_path)
