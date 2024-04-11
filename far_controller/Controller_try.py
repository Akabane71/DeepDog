import time
from pynput import keyboard

import send_msg as sm

# Dog_host
host = '192.168.1.101:5000'

pressed_keys = set()
pressed_once = set()

def on_press(key):
    global pressed_keys, pressed_once
    try:
        # 尝试将按键转换为字符串
        key_char = key.char
    except AttributeError:
        # 如果按键不是可打印字符，则使用特殊名称
        key_char = key.name

    try:
        if key_char == 'space':
            print('stand up')
        if key_char == 'w':
            if key_char not in pressed_keys:
                print('\t forward')
                sm.go_get_thread(host,'forward')
                pressed_keys.add(key_char)
                pressed_once.add(key_char)

        if key_char == 's':
            if key_char not in pressed_keys:
                print('\t back')
                sm.go_get_thread(host,'back')
                pressed_keys.add(key_char)
                pressed_once.add(key_char)

        if key_char == 'a':
            if key_char not in pressed_keys:
                print('\t left')
                sm.go_get_thread(host,'left')
                pressed_keys.add(key_char)
                pressed_once.add(key_char)

        if key_char == 'd':
            if key_char not in pressed_keys:
                print('\t right')
                sm.go_get_thread(host,'right')
                pressed_keys.add(key_char)
                pressed_once.add(key_char)
    except AttributeError:
        # 如果按下的是特殊按键，则输出特殊按键的名称
        if key == keyboard.Key.space:
            sm.go_get(host, 'standup')
            print('\tstand_up')

def on_release(key):
    global pressed_keys, pressed_once
    try:
        key_char = key.char
    except AttributeError:
        key_char = key.name

    # 监听释放按键，如果按下的是esc键，则停止监听
    if key == keyboard.Key.esc:
        print('结束监听...')
        return False

    # 持续控制的释放
    if key_char == 'w':
        if key_char in pressed_keys:
            print('\tstop forward')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)

    if key_char == 's':
        if key_char in pressed_keys:
            print('\tstop back')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)

    if key_char == 'a':
        if key_char in pressed_keys:
            print('\tstop left')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)

    if key_char == 'd':
        if key_char in pressed_keys:
            print('\tstop right')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)

if __name__ == '__main__':
    # 启动监听
    try:
        with keyboard.Listener(on_press=on_press,
                               on_release=on_release) as listener:
            print('开始监听')
            listener.join()
    except Exception as e:
        print('结束监听...')
