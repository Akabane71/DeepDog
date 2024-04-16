# 启动函数
import hong_run
import hong_save
from requeset_api import FromDog
from requeset_api import FromLocal

# 创建记录复现对象
h_run = hong_run.HongRun('./tmp/1.pkl')
h_save = hong_save.HongSave('./tmp/1.pkl')


if __name__ == '__main__':
    # h_save.main()
    # h_run.main()
    # area,signal,people = ToLocal.get_area_people_signal()

    # 区域
    # area = FromDog.get_area()
    # left_right = FromDog.get_left_or_right()
    # print(area)
    # print(left_right)
    # FromDog.send_dz_audio(area, left_right)

    # 救援区域播报
    area,signal,people = FromLocal.get_area_people_signal()
    FromDog.send_dxl_audio(area, signal, people)
