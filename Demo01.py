#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 11:58
# @Author  : Silvio27
# @Email   : silviosun@outlook.com
# @File    : Demo01.py
# @Software: PyCharm

import os
import time
import csv

fit_set_data = {
    '俯卧撑系列': {
        '分类': 'A',  # TODO A组即先下后上
        '清单': {
            'level1': {
                'name': '标准俯卧撑',
                'sets': 2,
                'repr': 10,
            },
            'level2': {
                'name': '窄距俯卧撑',
                'sets': 2,
                'repr': 10,
            },
            'level3': {
                'name': '单臂俯卧撑',
                'sets': 2,
                'repr': 10,
            },
        }

    },
    '深蹲系列':
        {
            'level1': {
                'name': '标准深蹲',
                'sets': 2,
                'repr': 50,
            },
            'level2': {
                'name': '窄距深蹲',
                'sets': 2,
                'repr': 40,
            },
            'level3': {
                'name': '单腿深蹲',
                'sets': 2,
                'repr': 20,
            },
        },
}


# TODO 锻炼计时模块

# TODO 数据读取写入

# TODO 锻炼类别项目

# TODO 锻炼记录












class WorkingSet(object):

    def __init__(self, data={}):
        self.proj = 'Base'
        self.data: dict = data

    def __str__(self):
        return f"锻炼内容{self.proj}"

    def get_all_data(self, data, i=0):
        for k, v in data.items():
            print('\t' * i, end='')
            if isinstance(v, dict):
                print(k)
                self.get_all_data(v, i + 1)
            else:
                print(f'{k}:{v}', end='\n')
            # TODO 之后是否用Return做返回值

    def show_sets_data(self):
        self.get_all_data(self.data)

    def show_sets_name(self):
        for index, item in enumerate(sorted(self.data.keys())):
            print(index, item)

    @staticmethod  # 静态变量，数据共享
    def aa():
        return 'aa'

    @classmethod
    def bb(cls):
        return 'bb'


class DealWithData(object):
    def __init__(self):
        self.path = 'exerice_recording.csv'

    def show_path(self):
        return f'zz{self.path}'


class DD(DealWithData):
    def __init__(self):
        self.path = 'DDpath'


    def show_path(self):
        return 'zz{self.path}'
        super().__init__()
        super().show_path()


class Push_Up(DD):
    def __init__(self):
        self.path = 'PUpath'


    def show_path(self):
        return f'zz{self.path}'
        super().__init__()
        super().show_path()

if __name__ == '__main__':
    # A = WorkingSet(fit_set_data['俯卧撑系列'])
    # A = WorkingSet(fit_set_data)
    # A.show_sets_name()

    B = Push_Up()
    print(Push_Up.__mro__)