import time
import pickle
import keyboard

"""
    记录宏操作
"""

class Hong():
    def __init__(self,path):
        # 保存的文件名称
        self.path = path

    def record_macro(self):
        print("开始记录宏，请按下键盘操作，按 '-' 键结束录制...")
        macro = []
        start_time = time.time()

        def on_key_event(event):
            if event.event_type == keyboard.KEY_DOWN and not keyboard.is_pressed('-'):
                timestamp = time.time() - start_time
                macro.append((timestamp, event.name))
                print(f"按键 {event.name} 已记录")

        keyboard.on_press(on_key_event)

        # 等待用户按下 'q' 键结束录制
        keyboard.wait('-')

        # 停止监听
        keyboard.unhook_all()

        return macro

    def save_macro(self,macro, filename):
        with open(filename, 'wb') as file:
            pickle.dump(macro, file)

    def main(self):
        macro = self.record_macro()
        self.save_macro(macro, self.path)

if __name__ == "__main__":
    h1 = Hong('macro.pkl')
    h1.main()
