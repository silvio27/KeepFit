# -*- coding: utf-8 -*-

import os
import time
import csv

path = 'exerice_recording.csv'

def write_record_csv(reps, sets, course, duration):
    with open(path, 'a', newline='', encoding='utf-8-sig') as file:
        csv_file = csv.writer(file)
        # data = ['时间戳', '日期时间', '锻炼项目', '个数', '组数', '持续时间']
        data = [time.time(), time.strftime('%Y-%m-%d %H:%M:%S'), course, reps, sets, duration]
        csv_file.writerow(data)


# 日期格式转换为时间戳,True表示23:59:59
def DateToTimeStramp(date, whole_day: bool = False):
    # 判断是否为日期格式
    if is_valid_date(date):
        TtoS = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        if whole_day != 0: TtoS = TtoS + 24 * 60 * 60 - 1
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TtoS)))
        return TtoS
    else:
        print("日期格式转换为时间戳错误，DateToTimeStramp")


# 判断是否是一个有效的日期字符串
def is_valid_date(str_date):
    try:
        time.strptime(str_date, "%Y-%m-%d")
        return True
    except Exception:
        print("日期格式错误请重新输入")
        return False

def WaitTime(t1 = 0):
    if t1 == 0:
        input_time = input("请输入等待开始时间(默认为5秒):")
        if type(input_time) != int or input_time == "":
            t1 = 5
    time.sleep(t1)



def StartTrain(reps: int = 25, sets: int = 2, m: int = 1, w: int = 1, remind: int = 10, breaktime: float = 1, course: str = '自由练习'):
    try:
        os.system('say "现在开始"')
        global starttime
        starttime = time.time()
        global r
        global t
        # r = 0
        # t = 0
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
                time.sleep(1)
            else:
                duration = round((time.time() - starttime) / 60, 1)
                print(duration)
                os.system('say "本次锻炼已完成，共锻炼 %s 分钟"' % duration)
                write_record_csv(reps=reps, sets=sets, course=course, duration=duration)
                break
            print("")
    except KeyboardInterrupt:
        print('ERR')
        duration = round((time.time() - starttime) / 60, 1)
        print(duration)
        write_record_csv(reps=reps * r + t, sets=1, course=course, duration=duration)


    except Exception as err:
        print('未知错误 %s' % (err))
    finally:
        print('Done')


# 锻炼情况概要
# TODO 后续可以增加每项运动的统计分析 主要针对 手臂、腿、腰腹、背部
# TODO 锻炼周期统计 开始结束时间，最近一周、一个月等 周期：3d 5d 7d 14d 30d etc

def Fit_Summary(startdate="1900-01-01", enddate="2099-12-31", with_today: bool = True):
    # TODO 统计总的平均时间，包含和不包含今天，再用一个函数调用统计，本函数只做一段周期内的统计
    a = []  # 日期
    b = []  # 日期&单项计时
    c = 0  # 计时求和用
    totally_time = 0
    m = []
    raw_data = []
    Summary_Startdate = DateToTimeStramp(startdate, False)
    Summary_enddate = DateToTimeStramp(enddate, with_today)
    with open(path)as f:
        f_csv = csv.reader(f)
        # 去除标题行
        next(f_csv)
        # 时间戳处理
        for l in f_csv:
            if Summary_Startdate <= float(l[0]) <= Summary_enddate:
                raw_data.append(l)
                a.append([time.strftime('%Y-%m-%d', time.localtime(float(l[0]))), l[5]])

        # 日期除出重并重新变为列表
        for r in raw_data:
            m.append(time.strftime('%Y-%m-%d', time.localtime(float(r[0]))))
        dt = list(set(m))
        dt.sort(reverse=True)

        for d in dt:
            for a1 in a:
                if d == a1[0]:
                    c += float(a1[1])
                    totally_time += float(a1[1])
            b.append([d, round(c, 1)])
            c = 0  # 统计时间清零

        work_detail = b
        workdays = len(dt)
        ave_time = totally_time / len(dt)

        Work_data = dict(work_detail=work_detail, workdays=workdays, ave_time=ave_time, totally_time = totally_time)
        return Work_data


# TODO 为保证均衡锻炼，对缺乏部分提醒功能

def Reminder_Do_More():
    pass

# TODO 摘要自动显示还是手动，自动显示的话是根据时间判断还是如今天锻炼次数超过4次，不足4次的情况下也需要提醒

def Reminder_Time(tt: int = 0, recent_day: int = 5):
    hour = int(time.strftime('%H'))
    startdate: str = '1900-01-01'
    today = time.strftime('%Y-%m-%d')
    if hour >= tt or hour == 0:
        today_detail = Fit_Summary(startdate=today, enddate=today, with_today=True)
        before_today_detail = Fit_Summary(startdate=startdate, enddate=today, with_today=False)

        print("今天的锻炼时间：%.2f 分钟" % (today_detail['ave_time']))
        print("平均锻炼时间：%.2f 分钟，共计 %.2f 分钟 " % (before_today_detail['ave_time'], before_today_detail['totally_time']))
        for i in before_today_detail['work_detail'][:recent_day]:
            print(i)


if __name__ == '__main__':

    # WaitTime(5)
    # StartTrain()
    # 俯卧撑系列
    # StartTrain(10, 2, 1, 1, 10, 0.5, '标准俯卧撑')  #标准俯卧撑2-12 窄距俯卧撑 #单臂俯卧撑
    # 深蹲系列
    # StartTrain(25, 2, 1, 1, 10, 0.5, '标准深蹲') #窄距深蹲 单腿深蹲
    # 引体向上
    # StartTrain(10, 2, 1, 1, 10, 0.5, '标准引体向上') #窄距引体向上') 单臂引体向上2-10
    # 举腿系列
    # StartTrain(20, 2, 1, 1, 10, 0.5, '平卧抬膝')  #平卧抬膝3-35   平卧屈举腿3-30   平卧蛙举腿3-25   平卧直举腿2-20
    # StartTrain(15, 2, 1, 1, 10, 0.5, '悬垂屈膝')  #悬垂抬膝   悬垂屈举腿   悬垂蛙举腿   悬垂直举腿2-30
    # 桥系列
    # StartTrain(20, 3, 1, 1, 10, 0.5, '短桥')    # 断桥 #直桥3-40 高低桥3-30 顶桥2-25  半桥2-20  标准桥2-15 下行桥2-10 上行桥2-8  合桥2-6   铁板桥2-30
    # StartTrain (10, 2, 1, 1, 10, 0.5, '直桥')

    Reminder_Time()

    # 倒立系列

    # Todo
    #   StartTrain(10, 2, 1, 1, 10, 0.5, '靠墙顶立') 2分钟  乌鸦式1分钟  靠墙倒立2分钟

    # StartTrain(20, 2, 1, 1, 10, 0.5, '半倒立撑')
    # StartTrain(15, 2, 1, 1, 10, 0.5, '标准倒立撑') #窄距倒立撑2-12 偏重倒立撑2-10 单臂倒立撑你2-8 杠杆倒立撑2-6 单臂倒立撑2-5

    # StartTrain(1, 1, 1, 10, 1, 0, '测试用')
    # 手动记录工作
    # write_record_csv(reps=20, sets=2, course='平卧抬膝', duration=3)

