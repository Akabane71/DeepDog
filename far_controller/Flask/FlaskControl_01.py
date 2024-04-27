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
    # 功能切换
    if key_char == 'space':
        sm.go_get(host, 'standup')
        print('\tstand_up')
    if key_char == 'r':
        sm.go_get(host, 'run')
        print('\trun')
    if key_char == 'f':
        sm.go_get(host, 'ladder')
        print('\tladder')
    if key_char == 'n':
        sm.go_get(host, 'walk')
        print('\twalk')
    if key_char == 'x':
        sm.go_get(host, 'stand')
        print('\tstand')
    if key_char == 'c':
        sm.go_get(host, 'clear')
        print('\tclear')

    #  强制结束生命
    if key_char == 'v':
        sm.go_get(host, 'stop_heart')
        print('\t stop_heart')

    # 自动踢球
    if key_char == 'b':
        sm.go_get(host, 'auto_ball')
        print('\t auto ball')

    if key_char == 'p':
        for i in range(3):
            sm.go_stand_up()
            time.sleep(1)
        print('\t dog stand up')

    # 切换摄像头
    # if key_char == 'tab':
    #     sm.go_get_thread(host,'/change_cap')
    #     print('tab')

    if key_char == '1':
        sm.go_get_thread(host,'1')
        print('\tmore 1')
    if key_char == '2':
        sm.go_get_thread(host,'2')
        print('\tmore 2')
    if key_char == '3':
        sm.go_get_thread(host,'3')
        print('\tmore 3')
    if key_char == '4':
        sm.go_get_thread(host,'4')
        print('\tmore 4')


    # 基础移动
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
            print('\t move_left')
            sm.go_get_thread(host,'move_left')
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 'd':
        if key_char not in pressed_keys:
            print('\t move_right')
            sm.go_get_thread(host,'move_right')
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 'q':
        if key_char not in pressed_keys:
            print('\t left')
            sm.go_get_thread(host,'turn_left')
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 'e':
        if key_char not in pressed_keys:
            print('\t right')
            sm.go_get_thread(host,'turn_right')
            pressed_keys.add(key_char)
            pressed_once.add(key_char)

    # up and down
    if key_char == 'i':
        if key_char not in pressed_keys:
            print('\t up')
            sm.go_get_thread(host,'up')
            pressed_keys.add(key_char)
            pressed_once.add(key_char)
    if key_char == 'k':
        if key_char not in pressed_keys:
            print('\t down')
            sm.go_get_thread(host,'down')
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
            sm.go_get_thread(host, 'stop_fb')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 's':
        if key_char in pressed_keys:
            print('\tstop back')
            sm.go_get_thread(host, 'stop_fb')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'a':
        if key_char in pressed_keys:
            print('\tstop move left')
            sm.go_get_thread(host, 'stop_move')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'd':
        if key_char in pressed_keys:
            print('\tstop move right')
            sm.go_get_thread(host, 'stop_move')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'q':
        if key_char in pressed_keys:
            print('\tstop left')
            sm.go_get_thread(host, 'stop_turn')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'e':
        if key_char in pressed_keys:
            print('\tstop right')
            sm.go_get_thread(host, 'stop_turn')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)

    # up and down
    if key_char == 'i':
        if key_char in pressed_keys:
            print('\tstop_ud')
            sm.go_get_thread(host, 'stop_ud')
            pressed_keys.remove(key_char)
            pressed_once.remove(key_char)
    if key_char == 'k':
        if key_char in pressed_keys:
            print('\tstop_ud')
            sm.go_get_thread(host, 'stop_ud')
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
