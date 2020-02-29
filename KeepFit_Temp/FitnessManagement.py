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


class Summary(object):
    pass



class FitnessManagement(object):

    def __init__(self):
        self.fitness_list_path = 'FitnessList.data'
        self.fitness_record_path = 'FitnessRecord.data'
        # self.fitness_record_path = 'Tempdata.data'
        self.fitness_list = []
        self.fitness_record =[]
        self.new_record = ''

    def __str__(self):
        return '健身管理系统'

    def show_all_data(self, data, i=0):
        for k, v in data.items():
            print('\t' * i, end='')
            if isinstance(v, dict):
                print(k)
                self.show_all_data(v, i + 1)
            else:
                print(f'{k}:{v}', end='\n')

    # 读取文件并转换成数据格式返回,看遍历这个在哪里进行处理
    def load_fitness_list(self):
        dD = DealWithData()
        data = dD.file_read(self.fitness_list_path)
        # self.show_all_data(data)
        # TODO 判断是字典还是列表，是否需要遍历
        # print(type(data))
        for i in data:
            self.fitness_list.append(i)

    # TODO 读取锻炼记录，添加到列表
    def load_fitness_record(self):
        dD = DealWithData()
        data = dD.file_read_csv(self.fitness_record_path)
        self.fitness_record = data


    # TODO 更新锻炼记录，直接追加即可
    def add_fitness_record(self):
        data = self.new_record
        dD = DealWithData()
        dD.file_write_csv(self.fitness_record_path, data)

    def amended_fitness_record(self, course='自由锻炼', reps=12, sets=1, duration=''):
        # 是否减少手动输入的情况，即不用按Enter
        course = input('选择课程[默认自由锻炼]:') or course
        reps = input('单组数量[默认12个]:') or reps
        sets = input('组数量[默认1组]:') or sets
        duration = round(reps * sets * 5 / 60, 2)
        duration = input('持续时间:[默认自动计算]') or duration
        print([time.time(), time.strftime('%Y-%m-%d %H:%M:%S'), course, reps, sets, duration])
        # self.new_record = [time.time(), time.strftime('%Y-%m-%d %H:%M:%S'), course, reps, sets, duration]
        # self.add_fitness_record()

    def start_training(self):

        course=''
        reps=''
        sets=''
        duration=''
        self.new_record = [time.time(), time.strftime('%Y-%m-%d %H:%M:%S'), course, reps, sets, duration]
        self.add_fitness_record()
        print('done')

    def timeCount(self):
        pass

    def run(self):
        # self.start_training()
        self.amended_fitness_record()
        # self.add_fitness_record()
        # self.load_fitness_record()
        # for i in self.fitness_record:
        #     print(i)
        # # self.load_fitness_list()
        # for i in enumerate(self.fitness_record):
        #     print(i)
        #
        # self.start_training()
        # self.add_fitness_record()
        # for i in enumerate(self.fitness_list):
        #     print(i)
        # print('准备开始训练')
        # aa = [item for item in self.fitness_list]
        # print(aa)
        #
        # meun_num = input('选择需要进行的项目:')
        # print(meun_num)

    @staticmethod
    def show_info():
        print('Game Start')


if __name__ == '__main__':
    FM = FitnessManagement()
    FM.run()