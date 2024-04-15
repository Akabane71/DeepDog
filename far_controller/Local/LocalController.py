import threading
import time
from pynput import keyboard

import send_msg as sm

"""
    本地控制机器狗 LocalContrDog
"""

# Dog_host
host = '192.168.1.101:5000'
# 运动主机的端口
server_address = ("192.168.1.120", 43893)

fb_val = 22600  # 前进速度
turn_val = 10000 # 转向速度
move_val = 30000 # 平移速度

pressed_keys = set()
pressed_once = set()

# 初始化控制对象
g = sm.GO(server_address)


def on_press(key):
    global pressed_keys, pressed_once
    try:
        # 尝试将按键转换为字符串
        key_char = key.char
    except AttributeError:
        # 如果按键不是可打印字符，则使用特殊名称
        key_char = key.name
    # 功能切换
    if key_char == 'space':
        g.go(msg=0x21010202,val=0)
        print('\tstand_up')

    if key_char == 'r':
        g.go(msg=0x21010307,val=fb_val)
        print('\nrun')

    if key_char == 'l':
        g.go(msg=0x21010401,val=0)
        print('\nladder')

    if key_char == 'j':
        g.go(msg=0x21010206,val=0)
        print('\nladder')

    if key_char == 'n':
        g.go(msg=0x21010300,val=0)
        print('\nwalk')
    if key_char == 'c':
        g.go(msg=0x21010c05,val=0)
        print('\nclear')

    # 增加切换摄像头功能
    # if key_char == 'tab':
    #     # sm.go_get(host, 'change_cap')
    #     print('\ncap changed')

    # 基础移动
    if key_char == 'w':
        if key_char not in pressed_keys:
            print('\t forward')
            g.go(msg=0x21010130,val=fb_val)
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 's':
        if key_char not in pressed_keys:
            print('\t back')
            g.go(msg=0x21010130,val=-fb_val)
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 'a':
        if key_char not in pressed_keys:
            print('\t move_left')
            g.go(msg=0x21010131,val=-move_val)
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 'd':
        if key_char not in pressed_keys:
            print('\t move_right')
            g.go(msg=0x21010131,val=move_val)
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 'q':
        if key_char not in pressed_keys:
            print('\t left')
            g.go(msg=0x21010135,val=-turn_val)
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 'e':
        if key_char not in pressed_keys:
            print('\t right')
            g.go(msg=0x21010135,val=turn_val)
            pressed_keys.add(key_char)
            pressed_once.add(key_char)


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
            g.go(msg=0x21010130,val=0)
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 's':
        if key_char in pressed_keys:
            print('\tstop back')
            g.go(msg=0x21010130,val=0)
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'a':
        if key_char in pressed_keys:
            print('\tstop move left')
            g.go(msg=0x21010131,val=0)
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'd':
        if key_char in pressed_keys:
            print('\tstop move right')
            g.go(msg=0x21010131,val=0)
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'q':
        if key_char in pressed_keys:
            print('\tstop left')
            g.go(msg=0x21010135, val=0)
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'e':
        if key_char in pressed_keys:
            print('\tstop right')
            g.go(msg=0x21010135,val=0)
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)

if __name__ == '__main__':
    # 启动生命
    threading.Thread(target=g.heart_exchange,args=(g.con,)).start()
    print('dog life 启动')
    # 启动监听
    try:
        with keyboard.Listener(on_press=on_press,
                               on_release=on_release) as listener:
            print('开始监听')
            listener.join()
    except Exception as e:
        print('结束监听...')
