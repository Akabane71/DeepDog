import time
import pickle
import pyautogui

"""
    执行宏文件
"""
class Hong():
    def __init__(self,path):
        self.path = path
    def execute_macro(self,macro):
        print("开始执行宏...")
        start_time = macro[0][0]  # 获取宏记录的起始时间

        for timestamp, key in macro:
            # 计算当前操作相对于起始时间的时间差，并等待
            elapsed_time = timestamp - start_time
            time.sleep(elapsed_time)

            # 执行键盘操作
            print(f'执行{key}')
            pyautogui.press(key)

        # 等待最后一个操作执行完成后再结束
        final_timestamp = macro[-1][0]
        total_elapsed_time = final_timestamp - start_time
        time.sleep(total_elapsed_time)

    def load_macro(self,filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def main(self):
        macro = self.load_macro(self.path)
        self.execute_macro(macro)

if __name__ == "__main__":
    h1 = Hong('./macro.pkl')
    h1.main()
