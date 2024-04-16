import time
import pickle
from pynput import keyboard

"""
    记录运动的脚本

    space 
"""

pressed_keys = set()
pressed_once = set()


class HongSave:
    def __init__(self, path):
        # 保存的文件名称
        self.path = path
    # 改变路径
    def change_path(self,path):
        self.path = path

    def record_macro(self):
        print("开始记录宏，请按下键盘操作，按 '-' 键结束录制...")
        macro = []
        start_time = time.time()

        def on_press(key):
            try:
                # 尝试将按键转换为字符串
                key_char = key.char
            except AttributeError:
                # 如果按键不是可打印字符，则使用特殊名称
                key_char = key.name
            try:
                # 检查按下的键是否为 '-' 键
                if key.char != '-':
                    if key_char not in pressed_keys:
                        pressed_keys.add(key_char)
                        pressed_once.add(key_char)
                        macro.append(('press', key_char, time.time() - start_time))
                        print(f"按键 {key_char} 已记录")
                else:
                    # 如果按下 '-' 键，则结束录制
                    return False
            except AttributeError:
                pass

        def on_release(key):
            try:
                # 尝试将按键转换为字符串
                key_char = key.char
            except AttributeError:
                # 如果按键不是可打印字符，则使用特殊名称
                key_char = key.name
            try:
                if key_char != '-':
                    if key_char in pressed_keys:
                        pressed_keys.remove(key_char)
                        pressed_once.remove(key_char)
                        macro.append(('release', key_char, time.time() - start_time))
                        print(f"release{key_char} 已记录")
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        return macro

    def save_macro(self, macro, filename):

        with open(filename, 'wb') as file:
            pickle.dump(macro, file)

    def main(self):
        macro = self.record_macro()
        self.save_macro(macro, self.path)


if __name__ == "__main__":
    h1 = HongSave('./tmp/1.pkl')
    h1.main()

