# -*- coding: utf-8 -*-

import os
import time
import csv

def write_record_csv(reps, sets, course, duration):
    path = 'exerice_recording.csv'
    with open(path, 'a', newline='', encoding='utf-8-sig') as file:
        csv_file = csv.writer(file)
        # data = ['时间戳', '日期时间', '锻炼项目', '个数', '组数', '持续时间']
        data = [time.time(), time.strftime('%Y-%m-%d %H:%M:%S'), course, reps, sets, duration]
        csv_file.writerow(data)

def StartTrain(reps: int = 25, sets: int = 1, m: int = 1, w: int = 1, remind: int = 10, breaktime: float = 1, course: str = '自由练习'):
    os.system('say "现在开始"')
    time.sleep(5)
    starttime: float = time.time()
    for r in range(sets):
        for t in range(reps):
            print(t + 1, end="\t")
            os.system('say "下"')
            time.sleep(m)
            os.system('say "坚持"')
            time.sleep(w)
            os.system('say "起"')
            time.sleep(m)

            if (t + 1) % remind == 0:
                os.system('say "已经完成 %s"' % str(t + 1))
        os.system('say "休闲 %s 分钟"' % breaktime)
        sleep_time = breaktime * 60 - 10
        if sleep_time > 0:
            time.sleep(breaktime * 60 - 10)  # 如果时间小于10秒

        if 0 < sets - r - 1:
            os.system('say "即将开始，还剩余 %s 次"' % str(sets - r - 1))
        else:
            duration = round((time.time() - starttime) / 60, 1)
            print(duration)
            os.system('say "本次锻炼已完成，共锻炼 %s 分钟"' % duration)
            write_record_csv(reps=reps, sets=sets, course=course, duration=duration)
            break
        print("")


if __name__ == '__main__':

    #俯卧撑系列
    # StartTrain(20, 3, 1, 1, 10, 0.5, '斜上俯卧撑')
    # StartTrain(20, 2, 1, 1, 10, 0.5, '标准俯卧撑')
    # StartTrain(20, 2, 1, 1, 10, 0.5, '窄距俯卧撑')
    # StartTrain(20, 2, 1, 1, 10, 0.5, '单臂俯卧撑')
    #深蹲系列
    StartTrain(10, 2, 1, 1, 10, 0.5, '标准深蹲')
    # StartTrain(20, 2, 1, 1, 10, 0.5, '窄距深蹲')
    # StartTrain(20, 2, 1, 1, 10, 0.5, '单腿深蹲')
    #引体向上
    # StartTrain(10, 2, 1, 1, 10, 0.5, '标准引体向上')
    # StartTrain(10, 2, 1, 1, 10, 0.5, '窄距引体向上')
    # StartTrain(6, 2, 1, 1, 10, 0.5, '单臂引体向上')
    #举腿系列
    # StartTrain(35, 3, 1, 1, 10, 0.5, '平卧抬膝')  #平卧抬膝3-35   平卧屈举腿3-30   平卧蛙举腿3-25   平卧直举腿2-20
    # StartTrain(15, 2, 1, 1, 10, 0.5, '悬垂屈膝')  #悬垂抬膝   悬垂屈举腿   悬垂蛙举腿   悬垂直举腿
    # StartTrain(30, 2, 1, 1, 10, 0.5, '悬垂直举腿')

    #桥系列
    # StartTrain(50, 3, 1, 1, 10, 0.5, '短桥')    #直桥3-40 高低桥3-30 顶桥2-25  半桥2-20  标准桥2-15 下行桥2-10 上行桥2-8  合桥2-6   铁板桥2-30
    #倒立系列

    # Todo
    #   StartTrain(10, 2, 1, 1, 10, 0.5, '靠墙顶立') 2分钟  乌鸦式1分钟  靠墙倒立2分钟

    # StartTrain(20, 2, 1, 1, 10, 0.5, '半倒立撑')
    # StartTrain(15, 2, 1, 1, 10, 0.5, '标准倒立撑') #窄距倒立撑2-12 偏重倒立撑2-10 单臂倒立撑你2-8 杠杆倒立撑2-6 单臂倒立撑2-5

    # StartTrain(1, 1, 1, 10, 1, 0, '测试用')
    # 手动记录工作
    # write_record_csv(reps=20, sets=2, course='平卧抬膝', duration=3)
    # write_record_csv(reps=10, sets=2, course='俯卧撑', duration=2)
    # write_record_csv(reps=10, sets=2, course='引体向上', duration=2)

