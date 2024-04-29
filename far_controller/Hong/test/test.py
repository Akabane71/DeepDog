import pickle
import time

from pynput.keyboard import Controller, Key
from pynput import keyboard

"""
    灵感来源
"""

class KeyRecorder():
    def __init__(self, filename):
        self.filename = filename
        self.recorded_keys = []
        self.should_stop = False

    def on_press(self, key):
        if hasattr(key, 'char'):
            self.recorded_keys.append(('press', key.char))
        else:
            self.recorded_keys.append(('press', str(key)))
        if str(key) == "'-'":  # 检查按键是否为 "-" 键
            self.should_stop = True  # 如果按下 "-" 键，设置退出标志为 True

    def on_release(self, key):
        try:
            self.recorded_keys.append(('release', key.char))
        except AttributeError:
            self.recorded_keys.append(('release', str(key)))

    def record_keys(self):
        print("开始记录按键操作，请按下键盘操作，按 '-' 键结束录制...")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while not self.should_stop:  # 持续监听，直到退出标志为 True
                time.sleep(0.1)
        print("按键操作记录完成！")

    def save_to_file(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.recorded_keys, file)
        print(f"按键操作已保存到文件 {self.filename}")

    def load_from_file(self):
        with open(self.filename, 'rb') as file:
            self.recorded_keys = pickle.load(file)
        print(f"从文件 {self.filename} 加载按键操作完成！")

    def execute_keys(self):
        print("开始执行按键操作...")
        keyboard = Controller()
        for action, key in self.recorded_keys:
            if action == 'press':
                print(f"按下键: {key}")
                keyboard.press(key)
                time.sleep(0.01)
            elif action == 'release':
                print(f"释放键: {key}")
                keyboard.release(key)
                time.sleep(0.01)
        print("按键操作执行完成！")

if __name__ == "__main__":
    recorder = KeyRecorder('recorded_keys.pkl')

    # 记录按键操作并保存到文件
    recorder.record_keys()
    recorder.save_to_file()

    # 从文件中加载按键操作并执行
    recorder.load_from_file()
    recorder.execute_keys()
