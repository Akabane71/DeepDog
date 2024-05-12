import time

import hong_run
import hong_save
import send_msg as sm
from requeset_api import FromDog
from requeset_api import FromLocal

host = '192.168.1.101:5000'
# 创建记录复现对象
h_run = hong_run.HongRun('./tmp/阶段1.pkl')
h_save = hong_save.HongSave('./tmp/左走.pkl')

ball = None

# 识别前进的道路并进行语音播报,返回要取的路
def identify_area():
    # 保险措施，防止没识别到
    area = 'a'
    left_right = 'left'
    try:
        area = FromDog.get_area() # qr码识别
        left_right = FromDog.get_left_or_right()
        print('area---> {},left_right---> {}'.format(area, left_right))
        FromDog.send_dz_audio(area, left_right)
        return area,left_right
    except Exception as e:
        print('no cap')
        return area,left_right

# 救援区域的识别 + 播报 + 动作
def rescue_area():
    try:
        # 救援区域播报
        area,signal,people = FromLocal.get_area_people_signal()
        print('area: {},signal: {},people: {}'.format(area,signal,people))
        FromDog.send_dxl_audio(area, signal, people)
    except Exception as e:
        # 如果出现了报错，就直接点头
        area = 'red'
        signal = 'water'
        people = 1
        print('area: {},signal: {},people: {}'.format(area,signal,people))
        FromDog.send_dxl_audio(area, signal, people)
    # 增加动作
    if people > 0:
        # 保险起见换为: 下蹲 + 动作 + 下蹲
        h_run.change('./tmp/点头.pkl')
        h_run.main()
    else:
        h_run.change('./tmp/摇头.pkl')
        h_run.main()


# 宏录制方案的脚本
def robot_cup_2024_g_run():
    # 起立
    sm.go_get(host, 'standup')
    print('\tstand_up')
    time.sleep(2)
    global ball
    # 前往qr码
    h_run.change('./tmp_g/step_1_g.pkl')
    h_run.main()

    # 识别qr码选择移动
    ball,lr = identify_area()

    # 右走
    if lr == "right":
        h_run.change('./tmp_g/step_2_right_1_g.pkl')
        h_run.main()
        time.sleep(2)
        h_run.change('./tmp_g/step_2_right_2_g.pkl')
        h_run.main()
    else:
        # 左走
        h_run.change('./tmp_g/step_2_left_1_g.pkl')
        h_run.main()
        time.sleep(2)
        h_run.change('./tmp_g/step_2_left_2_g.pkl')
        h_run.main()


    # 前往识别区域
    h_run.change('./tmp_g/step_3_vision_g.pkl')
    h_run.main()


    # 到达识别区域
    # 1. 第一个标志物
    rescue_area()
    time.sleep(2)
    # 向左移动一段距离
    h_run.change('./tmp_g/step_3_move_left_g.pkl')
    h_run.main()
    time.sleep(2)

    # 2.
    rescue_area()
    time.sleep(2)
    # 再左移
    h_run.change('./tmp_g/step_3_move_left_g.pkl')
    h_run.main()

    # 3.
    rescue_area()
    time.sleep(2)

    # 右转前往小球
    h_run.change('./tmp_g/step_4_go_to_ball_g.pkl')
    h_run.main()

    if ball == 'c':
        time.sleep(2)
        h_run.change('./tmp_g/step_5_ball_b_g.pkl')
        h_run.main()
    elif ball == 'b':
        time.sleep(2)
        h_run.change('./tmp_g/step_5_ball_left_g.pkl')
        h_run.main() # 左移一次
        time.sleep(1)
        h_run.change('./tmp_g/step_5_ball_b_g.pkl')
        h_run.main()
    elif ball == 'a':
        time.sleep(2)
        h_run.change('./tmp_g/step_5_ball_left_g.pkl')
        h_run.main()
        time.sleep(1)
        h_run.main() # 左移两次
        time.sleep(1)
        h_run.change('./tmp_g/step_5_ball_b_g.pkl')
        h_run.main()


# g狗的连续录制函数，从起点开始录制
def g_save():
    tmp_dir = 'tmp_dir'
    # 前往qr码
    h_save.change_path(f'./{tmp_dir}/step_1_g.pkl')
    print('step_1_g.pkl')
    h_save.main()
    time.sleep(2)

    # 识别qr码选择移动
    # ball, lr = identify_area()
    lr = 'left'
    # 右走
    if lr == "right":
        h_save.change_path(f'./{tmp_dir}/step_2_right_1_g.pkl')
        print('step_2_right_g.pkl')
        h_save.main()
        time.sleep(2)
    else:
        # 左走
        h_save.change_path(f'./{tmp_dir}/step_2_left_1_g.pkl')
        print('step_2_left_g.pkl')
        h_save.main()
        time.sleep(2)
    # 去视觉
    h_save.change_path(f'./{tmp_dir}/step_3_vision_g.pkl')
    print('step_3_vision_g.pkl')
    h_save.main()
    time.sleep(2)

    # 左移一小段
    h_save.change_path(f'./{tmp_dir}/step_3_move_left_g.pkl')
    print('step_3_move_left_g.pkl')
    h_save.main()
    time.sleep(2)

    # 左移一小段
    h_run.change(f'./{tmp_dir}/step_3_move_left_g.pkl')
    h_save.main()
    time.sleep(2)

    h_run.main()
    time.sleep(3)

    # 录制去小球
    h_save.change_path(f'./{tmp_dir}/step_4_go_to_ball_g.pkl')
    print('step_4_go_to_ball_g.pkl')
    h_save.main()
    time.sleep(2)

    # 左移
    h_save.change_path(f'./{tmp_dir}/step_5_move_left_g.pkl')
    print('step_5_move_left_g.pkl')
    h_save.main()

# g_动作，不加视觉
def g_run():
    # 前往qr码
    h_run.change('./tmp_g/step_1_g.pkl')
    h_run.main()
    time.sleep(2)

    # 识别qr码选择移动
    # ball, lr = identify_area()
    lr = 'left'
    # 右走
    if lr == "right":
        h_run.change('./tmp_g/step_2_right_g.pkl')
        h_run.main()
        time.sleep(2)
    else:
        # 左走
        h_run.change('./tmp_g/step_2_left_g.pkl')
        h_run.main()
        time.sleep(2)
    # 前往视觉区域 1
    h_run.change('./tmp_g/step_3_vision_g.pkl')
    h_run.main()
    time.sleep(2)

    # 左移一小段 2
    h_run.change('./tmp_g/step_3_move_left_g.pkl')
    h_run.main()
    time.sleep(2)

    # 再左移一段 2
    h_run.main()
    time.sleep(2)

    # 录制去小球
    h_run.change('./tmp_g/step_4_go_to_ball_g.pkl')
    h_run.main()
    time.sleep(1)

    # 左移
    h_run.change('./tmp_g/step_5_move_left_g.pkl')
    h_run.main()


if __name__ == '__main__':
    # _,_1 = identify_area()
    # rescue_area()
    # robot_cup_2024_g_run()
    # 测试
    g_save()
    # g_run()