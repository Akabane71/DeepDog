import time
from pynput import keyboard  # 第三方库
import send_msg as sm
host = '192.168.1.101:5000'

def on_press(key):
    try:
        # 尝试获取按下的按键并输出到控制台
        if key.char == 'w':
            time.sleep(0.2)
            print('\nforward')
            # sm.go()
        if key.char == 's':
            time.sleep(0.2)
            print('\tback')
        if key.char == 'a':
            time.sleep(0.2)
            print('\tleft')
        if key.char == 'd':
            time.sleep(0.2)
            print('\tright')
        if key.char == 'q':
            time.sleep(0.2)
            print('\theart_stop')
        if key.char == 'l':
            time.sleep(0.2)
            print('\t楼梯步态')
        if key.char == 'c':
            time.sleep(0.2)
            print('\tclear')

    except AttributeError:
        # 如果按下的是特殊按键，则输出特殊按键的名称
        if key == keyboard.Key.space:
            print('\tstand_up')

def on_release(key):
    # 监听释放按键，如果按下的是esc键，则停止监听
    if key == keyboard.Key.esc:
        print('退出监听...')
        return False



if __name__ == '__main__':
    # 启动监听
    try:
        with keyboard.Listener(on_press=on_press,
                               on_release=on_release) as listener:
            print('开始监听键盘输入...')
            listener.join()
    except Exception as e:
        print('终止')