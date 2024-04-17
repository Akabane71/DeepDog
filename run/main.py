import hong_run
import hong_save
from requeset_api import FromDog
from requeset_api import FromLocal

# 创建记录复现对象
h_run = hong_run.HongRun('./tmp/阶段1.pkl')
h_save = hong_save.HongSave('./tmp/左走.pkl')

ball = None

# 识别前进的道路,返回要取的路
def identify_area():
    area = FromDog.get_area()
    left_right = FromDog.get_left_or_right()
    print('area{},left_right{}'.format(area, left_right))
    FromDog.send_dz_audio(area, left_right)
    return area,left_right


# 救援区域的识别 + 播报 + 动作
def rescue_area():
    # 救援区域播报
    area,signal,people = FromLocal.get_area_people_signal()
    print('area{},signal{},people{}'.format(area,signal,people))
    FromDog.send_dxl_audio(area, signal, people)

    if people > 0:
        h_run.change('./tmp/点头.pkl')
        h_run.main()
    else:
        h_run.change('./tmp/摇头.pkl')
        h_run.main()


# 比赛启动的主要程序
def race():
    global ball
    # 过第一个楼梯
    h_run.change('./tmp/阶段1.pkl')
    h_run.main()
    ball,lr = identify_area()

    # 左走或者右走
    if lr == 'left':
        h_run.change('./tmp/左走.pkl')
        h_run.main()
    else:
        h_run.change('./tmp/右走.pkl')
        h_run.main()

    # 救援区域
    # 进行识别播报,左自动走一段距离

    # 校准一下 ----> 实现正对着危险标志
    # 1.
    rescue_area()
    h_run.change('./tmp/左走一段距离.pkl')
    h_run.main()

    # 2.
    rescue_area()
    h_run.main()
    # 3.
    rescue_area()
    h_run.main()

    # 前往踢球区域
    h_run.change('./tmp/前往踢球区域.pkl')
    if ball == 'c':
        # 自动踢球
        return
    if ball == 'b':
        # 往左走1格

        return
    if ball == 'a':
        # 往左走2格

        # auto(ball)
        return


if __name__ == '__main__':
    h_save.main()
    # rescue_area()
    # h_run.main()