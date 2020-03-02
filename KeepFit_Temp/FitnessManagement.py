#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/29 15:01
# @Author  : Silvio27
# @Email   : silviosun@outlook.com
# @File    : FitnessManagement.py
# @Software: PyCharm

# TODO 锻炼管理模块

import csv
import time
import os

class DealWithData(object):
    '''数据处理'''

    def __init__(self):
        pass

    def __str__(self):
        pass

    def file_read(self, path):
        with open(path, 'r', encoding='UTF-8') as f:
            data = f.read()
            # print(data)
            # 返回格式化数据,是否需要加Try，如果数据格式报错的话
            return eval(data)
            # return data

    def file_read_csv(self, path):
        with open(path)as f:
            f_csv = csv.reader(f)
            # 去除标题行
            next(f_csv)
            data = list(f_csv)
        return data


    def file_write(self, path, data=''):
        with open(path, 'a+', encoding='UTF-8') as f:
            f.write(str(data))
            print('已更新')

    def file_write_csv(self, path, data=''):
        """将练习记录写入CSV文档中"""
        with open(path, 'a', newline='', encoding='utf-8-sig') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(data)


class FitnessManagement(object):

    def __init__(self):
        self.fitness_list_path = 'FitnessList.data'
        self.fitness_record_path = 'FitnessRecord.data'
        # self.fitness_record_path = 'Tempdata.data'
        self.fitness_list = {}
        self.fitness_record =[]
        self.new_record = ''
        self.work_list =[]
        self.project_select = '俯卧撑系列'
        self.level_select = 'level1'
        self.break_time = 25


    def __str__(self):
        return '健身管理系统'

    def get_all_dict_data(self, data, i=0):
        for k, v in data.items():
            print('\t' * i, end='')
            if isinstance(v, dict):
                print(k)
                self.get_all_dict_data(v, i + 1)
            else:
                print(f'{k}:{v}', end='\n')


    def get_all_dict_data1(self, data, i=0):

        for f,v in data.items():
            print(f,end = ' ')
            for k,m in v['level'].items():
                print(k, end = ':')
                for n in m.values():
                    print( str(n), end =' ')
                print('', end='\t')
            print('')


    def show_all_dict_data(self):
        self.load_fitness_list()
        self.get_all_dict_data1(self.fitness_list['series'])

    # 读取文件并转换成数据格式返回,看遍历这个在哪里进行处理
    def load_fitness_list(self):
        dD = DealWithData()
        data = dD.file_read(self.fitness_list_path)
        # self.show_all_data(data)
        # TODO 判断是字典还是列表，是否需要遍历
        # print(type(data))
        self.fitness_list = data

    # TODO 读取锻炼记录，添加到列表
    def load_fitness_record(self):
        dD = DealWithData()
        data = dD.file_read_csv(self.fitness_record_path)
        self.fitness_record = data
        return data

    # TODO 显示全部锻炼数据
    def show_all_record(self):
        for d in self.load_fitness_record():
            print(d)

    # 日期格式转换为时间戳,True表示23:59:59
    def date_to_timestramp(self, date, whole_day: bool = False):
        # 判断是否为日期格式
        if self.is_valid_date(date):
            TtoS = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
            if whole_day != 0: TtoS = TtoS + 24 * 60 * 60 - 1
            # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TtoS)))
            return TtoS
        else:
            print("日期格式转换为时间戳错误，DateToTimeStramp")

    # 判断是否是一个有效的日期字符串
    def is_valid_date(self, str_date):
        try:
            time.strptime(str_date, "%Y-%m-%d")
            return True
        except Exception:
            print("日期格式错误请重新输入")
            return False

    def fit_summary(self, startdate="1900-01-01", enddate="2099-12-31", with_today: bool = True):
        # TODO 统计总的平均时间，包含和不包含今天，再用一个函数调用统计，本函数只做一段周期内的统计
        a = []  # 日期
        b = []  # 日期&单项计时
        c = 0  # 计时求和用
        totally_time = 0
        m = []
        raw_data = []
        Summary_Startdate = self.date_to_timestramp(startdate, False)
        Summary_enddate = self.date_to_timestramp(enddate, with_today)
        for l in self.load_fitness_record():
            if l == []: continue  # 如果发现csv中有空行，自动跳过
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

    def reminder_time(self, tt: int = 0, recent_day: int = 5):
        hour = int(time.strftime('%H'))
        startdate: str = '1900-01-01'
        today = time.strftime('%Y-%m-%d')
        if hour >= tt or hour == 0:
            before_today_detail = self.fit_summary(startdate=startdate, enddate=today, with_today=False)
            today_detail = self.fit_summary(startdate=today, enddate=today, with_today=True)

            print("今天的锻炼时间：%.2f 分钟" % (today_detail['ave_time']))
            print("平均锻炼时间：%.2f 分钟，共计 %.2f 分钟 " % (before_today_detail['ave_time'], before_today_detail['totally_time']))
            for i in before_today_detail['work_detail'][:recent_day]:
                print(i)

    # TODO 更新锻炼记录，直接追加即可
    def add_fitness_record(self):
        data = self.new_record
        dD = DealWithData()
        dD.file_write_csv(self.fitness_record_path, data)

    def amended_fitness_record(self,course='自由锻炼', reps=12, sets=1, duration=''):
        # TODO 日期可能会存在格式错误的问题，错误的情况下反馈None，需要继续测试
        date = input('输入日XXXX-XX-XX Enter=Today:') or time.strftime('%Y-%m-%d')
        course = input(f'选择课程在[{course}]:') or course
        reps = input(f'单组数量[{reps}]:') or reps
        sets = input(f'组数量[{sets}]:') or sets
        duration = round(int(reps) * int(sets) * 5 / 60, 2)
        duration = input(f'持续时间:[{duration}]') or duration
        print([str(self.date_to_timestramp(date)) + '.000000', date + ' 00:00:00', course, reps, sets, duration])
        self.new_record = [str(self.date_to_timestramp(date)) + '.000000', date + ' 00:00:00', course, reps, sets, duration]
        self.add_fitness_record()

    def reps_say_count(self):
        # TODO 需要读取fitness_list的原始数据，如果出错可能 load 失败self.load_fitness_list()
        self.work_list = self.fitness_list['series'][self.project_select]
        for k, v in self.fitness_list['saytime'][self.work_list['work_type']].items():
            os.system(f'say "{k}"')
            time.sleep(v)

    def start_training(self):
        self.load_fitness_list()
        start_time = time.time()

        self.work_list = self.fitness_list['series'][self.project_select]
        # print(self.work_list)
        course = self.work_list['level'][self.level_select]['name']
        reps = self.work_list['level'][self.level_select]['reps']
        sets = self.work_list['level'][self.level_select]['sets']
        os.system(f'say "～开始{course},{sets}组{reps}个"')
        for s in range(sets):
            for r in range(reps):
                print(r+1, end=' ')
                self.reps_say_count()
                if r + 1 < reps:
                    if (r + 1) % 10 == 0 and r + 1 < reps:
                        os.system(f'say "已经完成{r + 1}"')
            if s + 1 < sets:
                os.system('say "休闲30秒"')
                # TODO 修改休闲时间
                time.sleep(self.break_time)
                print('')
                os.system(f'say "准备开始第{s + 2}组"')

        os.system('say "已完成锻炼"')
        print('')

        duration = round((time.time() - start_time) / 60, 2)
        print(f'{course},{reps},{sets},{duration}')
        self.new_record = [time.time(), time.strftime('%Y-%m-%d %H:%M:%S'), course, reps, sets, duration]
        self.add_fitness_record()
        print('数据已记录')
        # self.reminder_time()


    def train_set(self, project='俯卧撑系列', level = 1):
        self.project_select = project
        self.level_select = 'level' + str(level)
        self.start_training()
        time.sleep(self.break_time)

    def morning_training(self):
        os.system('say "Start"')
        time.sleep(10)
        for i in range(2):
            self.train_set(project='俯卧撑系列', level=1)
            self.train_set(project='举腿系列', level=1)
            self.train_set(project='桥系列', level=2)

        self.train_set(project='桥系列', level=1)
        self.train_set(project='深蹲系列', level=1)
        self.train_set(project='深蹲系列', level=2)



    def night_training(self):
        os.system('say "Start"')
        time.sleep(10)
        # self.train_set(project='深蹲系列', level=2)
        # for i in range(2):
        #     self.train_set(project='俯卧撑系列', level=1)
        #     self.train_set(project='举腿系列', level=1)
        #     self.train_set(project='桥系列', level=2)
        self.train_set(project='俯卧撑系列', level=1)
        self.train_set(project='桥系列', level=1)
        self.train_set(project='深蹲系列', level=1)


        # self.train_set(project='俯卧撑系列', level=1)
        # self.train_set(project='举腿系列', level=1)
        # self.train_set(project='桥系列', level=2)
        # self.train_set(project='深蹲系列', level=1)


    def run(self):
        # self.show_all_dict_data()
        # pass
        # os.system('say "Start"')
        # time.sleep(10)
        # self.train_set(project='俯卧撑系列', level=1)
        # self.train_set(project='俯卧撑系列', level=1)
        # self.train_set(project='举腿系列', level=1)
        # self.train_set(project='桥系列', level=2)
        # self.train_set(project='深蹲系列', level=1)
        self.night_training()
        # self.morning_training()
        self.reminder_time()

    @staticmethod
    def show_info():
        print('Game Start')
        print('''俯卧撑系列\深蹲系列\举腿系列\桥系列\引体向上系列''')


"""
俯卧撑系列  level1:标准俯卧撑 1 12 	level2:标准俯卧撑 2 10 	level3:窄距俯卧撑 2 10 	level4:单臂俯卧撑 2 10 	
深蹲系列    level1:标准深蹲 1 50 	level2:窄距深蹲 1 40 	level3:单腿深蹲 2 20 	
举腿系列    level1:平卧屈举腿 1 12 	level2:平卧屈举腿 2 20 	level3:平卧屈举腿 2 30 	
桥系列        level1:短桥 1 50 	level2:直桥 1 12 	level3:直桥 2 20 	
引体向上系列 level1:标准引体向上 1 12 	level2:窄距引体向上 2 12 	level3:单臂引体向上 2 8 	
"""
if __name__ == '__main__':
    FM = FitnessManagement()
    FM.run()
    # FM.show_all_dict_data()