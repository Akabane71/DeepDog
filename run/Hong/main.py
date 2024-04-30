import time

import hong_run
import hong_save
import send_msg as sm
from requeset_api import FromDog
from requeset_api import FromLocal


# 创建记录复现对象
h_run = hong_run.HongRun('./tmp/阶段1.pkl')
h_save = hong_save.HongSave('./tmp/左走.pkl')

ball = None

# 识别前进的道路并进行语音播报,返回要取的路
def identify_area():
    area = FromDog.get_area()
    left_right = FromDog.get_left_or_right()
    print('area--->{},left_right--->{}'.format(area, left_right))
    FromDog.send_dz_audio(area, left_right)
    return area,left_right


# 救援区域的识别 + 播报 + 动作
def rescue_area():
    # 救援区域播报
    area,signal,people = FromLocal.get_area_people_signal()
    print('area: {},signal: {},people: {}'.format(area,signal,people))
    FromDog.send_dxl_audio(area, signal, people)

    # 增加动作
    if people > 0:
        h_run.change('./tmp/点头.pkl')
        h_run.main()
    else:
        h_run.change('./tmp/摇头.pkl')
        h_run.main()


# 宏录制方案的脚本
def robot_cup_2024():
    global ball
    # 前往qr码
    h_run.change('./tmp/step_1.pkl')
    h_run.main()

    # 识别qr码选择移动
    ball,lr = identify_area()

    # 右走
    if lr == "right":
        h_run.change('./tmp/step_2_right.pkl')
        h_run.main()
    else:
        # 左走
        h_run.change('./tmp/step_2_left.pkl')
        h_run.main()

    # 到达识别区域
    # 1. 第一个标志物
    rescue_area()
    time.sleep(2)
    # 向左移动一段距离
    h_run.change('./tmp/move_left.pkl')
    h_run.main()

    # 2
    rescue_area()
    time.sleep(2)
    h_run.main()

    # 3
    rescue_area()
    time.sleep(2)

    # 右转前往小球
    h_run.change('./tmp/go_to_ball.pkl')
    h_run.main()

    h_run.main()
    if ball == 'c':
        h_run.change('./tmp/ball_1.pkl')
        h_run.main()
    elif ball == 'b':
        # 左转移动一定距离再右转,踢球
        h_run.change('./tmp/ball_2.pkl')
        h_run.main()
    elif ball == 'a':
        h_run.change('./tmp/ball_3.pkl')
        h_run.main()


if __name__ == '__main__':
    # 前往qr码
    h_run.change('./tmp/step_1.pkl')
    h_run.main()

    # 识别qr码选择移动
    ball, lr = identify_area()
    # 右走
    if lr == "right":
        h_run.change('./tmp/step_2_right.pkl')
        h_run.main()
    else:
        # 左走
        h_run.change('./tmp/step_2_left.pkl')
        h_run.main()