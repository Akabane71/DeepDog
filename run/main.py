import time

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

    # 增加动作
    if people > 0:
        h_run.change('./tmp/点头.pkl')
        h_run.main()
    else:
        h_run.change('./tmp/摇头.pkl')
        h_run.main()


if __name__ == '__main__':
    pass