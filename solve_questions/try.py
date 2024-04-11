import keyboard

pressed_keys = set()
pressed_once = set()

def on_key_event(event):
    global pressed_keys, pressed_once
    if event.event_type == keyboard.KEY_DOWN:
        if event.name =='space':
            print('stand up')

        if event.name not in pressed_keys:
            if event.name == 'w':
                print(f"\tforward")
                pressed_keys.add(event.name)
                pressed_once.add(event.name)
            if event.name == 's':
                print(f"\tback")
                pressed_keys.add(event.name)
                pressed_once.add(event.name)
            if event.name == 'a':
                print(f"\tleft")
                pressed_keys.add(event.name)
                pressed_once.add(event.name)
            if event.name == 'd':
                print(f"\tright")
                pressed_keys.add(event.name)
                pressed_once.add(event.name)

    elif event.event_type == keyboard.KEY_UP:
        if event.name in pressed_keys:
            if event.name == 'w':
                print(f"\tforward")
                pressed_keys.remove(event.name)
                pressed_once.remove(event.name)
            if event.name == 's':
                print(f"\tback")
                pressed_keys.remove(event.name)
                pressed_once.remove(event.name)
            if event.name == 'a':
                print(f"\tleft")
                pressed_keys.remove(event.name)
                pressed_once.remove(event.name)
            if event.name == 'd':
                print(f"\tright")
                pressed_keys.remove(event.name)
                pressed_once.remove(event.name)

keyboard.hook(on_key_event)

while True:
    for key in pressed_once:
        print(f"键盘按键 {key} 被按下")
    pressed_once.clear()
    keyboard.wait('esc')
