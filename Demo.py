#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import csv

path = 'exerice_recording.csv'
# starttime = time.time()


def write_record_csv(reps, sets, course, duration):
    """将练习记录写入CSV文档中"""
    with open(path, 'a', newline='', encoding='utf-8-sig') as file:
        csv_file = csv.writer(file)
        # data = ['时间戳', '日期时间', '锻炼项目', '个数', '组数', '持续时间']
        data = [time.time(), time.strftime('%Y-%m-%d %H:%M:%S'), course, reps, sets, duration]
        csv_file.writerow(data)


def write_record_csv_amend(reps, sets, course='自由锻炼', per_rep_time=5, date=time.strftime('%Y-%m-%d')):
    with open(path, 'a', newline='', encoding='utf-8-sig') as file:
        csv_file = csv.writer(file)
        # data = ['时间戳', '日期时间', '锻炼项目', '个数', '组数', '持续时间']
        data = [str(date_to_timestramp(date)) + '.000000', date + ' 00:00:00', course, reps, sets,
                reps * sets * per_rep_time]
        csv_file.writerow(data)


def record_by_hand(reps, sets, course='自由锻炼', per_rep_time='5'):
    write_record_csv(reps, sets, course, duration=reps * sets * per_rep_time)


# 日期格式转换为时间戳,True表示23:59:59
def date_to_timestramp(date, whole_day: bool = False):
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


def wait_time(t1=0):
    if t1 == 0:
        input_time = input("请输入等待开始时间(默认为5秒):")
        if type(input_time) != int or input_time == "":
            t1 = 5
    time.sleep(t1)


def start_train(reps: int = 25, sets: int = 2, um: int = 1, dm: int = 1, w: int = 1, remind: int = 10,
                breaktime: float = 1, course: str = '自由练习'):

    global starttime
    starttime = time.time()
    try:
        # os.system('say "现在开始"')
        os.system(f'say "～开始{course},{sets}组{reps}个"')

        global r
        global t
        # r = 0
        # t = 0
        for r in range(sets):
            for t in range(reps):
                print(t + 1, end="\t")
                os.system('say "下"')
                time.sleep(um)
                os.system('say "坚持"')
                time.sleep(w)
                os.system('say "起"')
                time.sleep(dm)
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

def fit_summary(startdate="1900-01-01", enddate="2099-12-31", with_today: bool = True):
    # TODO 统计总的平均时间，包含和不包含今天，再用一个函数调用统计，本函数只做一段周期内的统计
    a = []  # 日期
    b = []  # 日期&单项计时
    c = 0  # 计时求和用
    totally_time = 0
    m = []
    raw_data = []
    Summary_Startdate = date_to_timestramp(startdate, False)
    Summary_enddate = date_to_timestramp(enddate, with_today)
    with open(path)as f:
        f_csv = csv.reader(f)
        # 去除标题行
        next(f_csv)
        # 时间戳处理
        for l in f_csv:
            if l == []:continue # 如果发现csv中有空行，自动跳过
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
        if workdays != 0:  # 如果今天没有锻炼，避免由于统计时工作天数位0而报错
            ave_time = totally_time / len(dt)
        else:
            ave_time = 0

        Work_data = dict(work_detail=work_detail, workdays=workdays, ave_time=ave_time, totally_time=totally_time)
        return Work_data


# TODO 为保证均衡锻炼，对缺乏部分提醒功能

def reminder_do_more():
    pass


# TODO 摘要自动显示还是手动，自动显示的话是根据时间判断还是如今天锻炼次数超过4次，不足4次的情况下也需要提醒

def reminder_time(tt: int = 0, recent_day: int = 5):
    hour = int(time.strftime('%H'))
    startdate: str = '1900-01-01'
    today = time.strftime('%Y-%m-%d')
    if hour >= tt or hour == 0:
        before_today_detail = fit_summary(startdate=startdate, enddate=today, with_today=False)
        today_detail = fit_summary(startdate=today, enddate=today, with_today=True)


        print("今天的锻炼时间：%.2f 分钟" % (today_detail['ave_time']))
        print("平均锻炼时间：%.2f 分钟，共计 %.2f 分钟 " % (before_today_detail['ave_time'], before_today_detail['totally_time']))
        for i in before_today_detail['work_detail'][:recent_day]:
            print(i)

def night_exe_list():
    wait_time(10)
    start_train(8, 2, 1, 1, 1, 10, 0.5, '标准俯卧撑')
    wait_time(30)
    start_train(12, 2, 1, 1, 1, 10, 0.5, '直桥')
    wait_time(30)
    start_train(12, 2, 2, 2, 1, 10, 0.5, '平卧屈举腿')
    wait_time(30)
    start_train(30, 2, 1, 1, 1, 10, 0.5, '短桥')
    wait_time(30)
    start_train(10, 1, 1, 1, 1, 10, 0.5, '标准俯卧撑')
    wait_time(30)
    start_train(12, 1, 2, 2, 1, 10, 0.5, '平卧屈举腿')
    # TODO 暂停判断，是否结束，如果一段时间没有操作，则继续进程

def morning_exe_list_easy():

    wait_time(10)
    # for i in range(2):
    #     start_train(10, 1, 1, 1, 1, 100, 0.5, '标准俯卧撑')
    #     # wait_time(30)
    #     start_train(12, 1, 1, 1, 1, 100, 0.5, '直桥')
    #     # wait_time(30)
    #     start_train(12, 1, 2, 2, 1, 100, 0.5, '平卧屈举腿')
    #
    # start_train(30, 1, 1, 1, 1, 15, 0.5, '标准深蹲')
    start_train(30, 1, 1, 1, 1, 15, 0.5, '窄距深蹲')


# TODO 暂停判断，是否结束，如果一段时间没有操作，则继续进程def night_exe_list_easy():
#         wait_time(10)
#         for i in range(2):
#             # wait_time(30)
#             start_train(12, 1, 1, 1, 1, 10, 0.5, '直桥')
#             # wait_time(30)
#             start_train(12, 1, 2, 2, 1, 10, 0.5, '平卧屈举腿')
#         start_train(8, 1, 1, 1, 1, 10, 0.5, '标准俯卧撑')
#         start_train(30, 1, 1, 1, 1, 10, 0.5, '窄距深蹲')

if __name__ == '__main__':
    # wait_time(10)
    # morning_exe_list_easy()
    # start_train()
    # 俯卧撑系列
    # start_train(8, 2, 1, 1, 1, 10, 0.5, '标准俯卧撑')  #标准俯卧撑2-12 窄距俯卧撑 #单臂俯卧撑
    # 深蹲系列
    # start_train(30, 3, 1, 1, 1, 10, 0.5, '标准深蹲') #窄距深蹲 单腿深蹲
    # 举腿系列
    # wait_time(30)
    # start_train(12, 2, 2, 2, 1, 10, 0.5, '平卧屈举腿')  #平卧抬膝3-35   平卧屈举腿3-30    # start_train(15, 2, 2, 2, 1, 10, 0.5, '悬垂屈膝')  #悬垂抬膝   悬垂屈举腿   悬垂蛙举腿   悬垂直举腿2-30
    # start_train(8, 1, 2, 4, 1, 10, 0.5, '平卧蛙举腿') #平卧蛙举腿3-25   平卧直举腿1-5 to 2-20
    # 桥系列
    # start_train(40, 2, 1, 1, 1, 10, 0.5, '短桥')    # 断桥 #直桥3-40 高低桥3-30 顶桥2-25  半桥2-20  标准桥2-15 下行桥2-10 上行桥2-8  合桥2-6   铁板桥2-30
    # wait_time(30)
    # start_train(12, 2, 1, 1, 1, 10, 0.5, '直桥')
    # wait_time(30)
    # start_train(50, 3, 1, 1, 1, 10, 0.5, '短桥')
    # wait_time(30)
    # start_train(8, 1, 1, 1, 1, 10, 0.5, '标准俯卧撑')
    # 引体向上
    # start_train(10, 2, 1, 1, 1, 10, 0.5, '标准引体向上') #窄距引体向上') 单臂引体向上2-10

    reminder_time()

    # 倒立系列

    # Todo
    #   start_train(10, 2, 1, 1, 1, 10, 0.5, '靠墙顶立') 2分钟  乌鸦式1分钟  靠墙倒立2分钟

    # start_train(20, 2, 1, 1, 1, 10, 0.5, '半倒立撑')
    # start_train(15, 2, 1, 1, 1, 10, 0.5, '标准倒立撑') #窄距倒立撑2-12 偏重倒立撑2-10 单臂倒立撑你2-8 杠杆倒立撑2-6 单臂倒立撑2-5

    # start_train(1, 1, 1, 1, 10, 1, 0, '测试用')
    # 手动记录工作
    # write_record_csv(reps=20, sets=2, course='平卧抬膝', duration=3)
    # record_by_hand(6, 1, '标准引体向上', 5)
    #手动记录，当不记得时间的情况下补录数据
    # write_record_csv_amend(reps=100, sets=99, course='自由锻炼', per_rep_time=5, date='2020-02-22')
