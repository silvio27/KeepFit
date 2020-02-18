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



def StartTrain(reps: int = 25, sets: int = 1, m: int = 1, w: int = 1, remind: int = 10, breaktime: float = 1,
               course: str = '自由练习'):
    try:
        os.system('say "现在开始"')
        global starttime
        starttime = time.time()
        global r
        global t
        r = 0
        t = 0
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
    except KeyboardInterrupt:
        print('ERR')
        duration = round((time.time() - starttime) / 60, 1)
        print(duration)
        write_record_csv(reps=reps * r + t, sets=1, course=course, duration=duration)


    except Exception as err:
        print('未知错误 %s' % (err))
    finally:
        print('Done')



def WaitTime(t1=0):
    if t1 == 0:
        t = input("请输入等待开始时间(默认为5秒):")
        if type(t) != int or t == "":
            t1 = 5
    time.sleep(t1)



#锻炼情况概要
#TODO 后续可以增加每项运动的统计分析 主要针对 手臂、腿、腰腹、背部

#TODO 锻炼周期统计 开始结束时间，最近一周、一个月等

#TODO 摘要自动显示还是手动，自动显示的话是根据时间判断还是如今天锻炼次数超过4次，不足4次的情况下也需要提醒
def Fit_Summary():
    a = [] #日期
    b = []  #日期&单项计时
    c = 0 #计时求和用
    tongji = []
    with open(path)as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            a.append(row[1][:10])
            b.append([row[1][:10],row[5]])
        dt = list(set(a))   #日期除出重并重新变为列表
        dt.sort(reverse=True)
        # print(dt[0])
        dt.remove('日期时间')
        a = dt  #除重后的日期列表
        #对日期锻炼时间求和
        for a1 in a:
            for b1 in b:
                if a1 == b1[0]:
                    c += float(b1[1])
            tongji.append([a1, c])
            c = 0 #统计时间清零
        ave = 0
        day = 0
        for t in tongji:
            day += 1
            ave += t[1]
        ave = ave/day
        todayt = tongji[0][1]
        print("今天锻炼了：%.2f 分钟，平均 %.2f 分钟，共锻炼: %d 天" % (todayt, ave, day)) #TODO 自由今天锻炼了日期才会更新，不然日期为最近一天，可以增加对统计时间和NOW判断
        ca = ave - todayt
        if ca > 0:
            print("距离平均时间差 %.2f 分钟, 快看看在再哪里可以再锻炼一下" % ca) #TODO 给出锻炼哪方面的建议？
        elif ca < 0:
            print("超过平均时间差 %.2f 分钟" % abs(ca))
        else:
            print("和平均水平一致") #TODO 是否要去除今天的时间，今天时间低的话会拉低平均锻炼时间

        #统计详情
        # for t in tongji:
        #     print(t)
        #展示最近5天的统计详情
        for t in tongji[:5]:
            print(t)

#TODO 为保证均衡锻炼，对缺乏部分提醒功能
def Reminder():
    pass

if __name__ == '__main__':
    # WaitTime(5)
    Fit_Summary()

    # 俯卧撑系列
    # StartTrain(10, 2, 1, 1, 10, 0.5, '标准俯卧撑')  #标准俯卧撑2-12 窄距俯卧撑 #单臂俯卧撑

    # 深蹲系列
    # StartTrain(20, 4, 1, 1, 10, 0.5, '标准深蹲') #窄距深蹲 单腿深蹲

    # 引体向上
    # StartTrain(10, 2, 1, 1, 10, 0.5, '标准引体向上') #窄距引体向上') 单臂引体向上2-10

    # 举腿系列
    # StartTrain(21, 2, 1, 1, 10, 0.5, '平卧抬膝')  #平卧抬膝3-35   平卧屈举腿3-30   平卧蛙举腿3-25   平卧直举腿2-20
    # StartTrain(15, 2, 1, 1, 10, 0.5, '悬垂屈膝')  #悬垂抬膝   悬垂屈举腿   悬垂蛙举腿   悬垂直举腿2-30

    # 桥系列
    # StartTrain(12, 2, 1, 1, 10, 0.5, '直桥')    #直桥3-40 高低桥3-30 顶桥2-25  半桥2-20  标准桥2-15 下行桥2-10 上行桥2-8  合桥2-6   铁板桥2-30

    # 倒立系列
    '''
    # Todo
    #   StartTrain(10, 2, 1, 1, 10, 0.5, '靠墙顶立') 2分钟  乌鸦式1分钟  靠墙倒立2分钟

    # StartTrain(20, 2, 1, 1, 10, 0.5, '半倒立撑')
    # StartTrain(15, 2, 1, 1, 10, 0.5, '标准倒立撑') #窄距倒立撑2-12 偏重倒立撑2-10 单臂倒立撑你2-8 杠杆倒立撑2-6 单臂倒立撑2-5
    '''

    # StartTrain(1, 1, 1, 10, 1, 0, '测试用')
    # 手动记录工作
    # write_record_csv(reps=20, sets=2, course='平卧抬膝', duration=3)
