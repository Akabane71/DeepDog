import time
import pickle
from pynput.keyboard import Controller

"""
    宏播放函数
        误差在0.1s内
"""

key_press = None
key_release = None


class HongRun:
    def __init__(self, path):
        self.path = path
    # 更换path
    def change(self,path):
        self.path = path
    # 切换下一个脚本
    def load(self,path):
        self.path = path

    def execute_macro(self, macro):
        print("开始执行宏...")
        start_time = float(macro[0][2])  # 获取宏记录的起始时间
        keyboard = Controller()
        c = False
        t1 = time.time()
        for way, key, timestamp in macro:
            elapsed_time = timestamp - start_time
            start_time = timestamp
            if c is False:
                c = True
            else:
                time.sleep(elapsed_time)
            # 开始第一个运动
            if way == 'press':
                # Thread(target=keyboard.press,args=(key,)).start()
                keyboard.press(key)
                # print('press\t',key)
            if way == 'release':
                keyboard.release(key)
                # Thread(target=keyboard.release, args=(key,)).start()
                # print('release\t',key)
        t2 = time.time()
        print('total:',t2-t1)
    def load_macro(self, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def main(self):
        macro = self.load_macro(self.path)
        self.execute_macro(macro)

if __name__ == "__main__":
    h1 = HongRun('./tmp_g/step_2_left_g.pkl')
    h1.main()


