"""
配置文件和数据整理。
"""

import configparser
import json
import os.path

import pandas as pd
from loguru import logger


def get_with_json_index(num=1):
    """
    通过班级序号获取学生信息。

    :param num: 班级序号
    :return: 学生信息
    """
    students = get_all_students()
    if students == {} or students['students'] == {}:
        return {'short_id': '', 'id': '000000', 'name': '无结果'}
    for student in students['students']:
        if student['short_id'] == num:
            return student
    return None


def get_with_id(num=1):
    """
    通过学校全局学号获取学生信息。

    :param num: 全局学号
    :return: 学生信息
    """
    students = get_all_students()
    if students == {} or students['students'] == {}:
        return {'weight': '1', 'id': '000000', 'name': '无结果'}
    for student in students['students']:
        if student['id'] == num:
            return student
    return None


def get(num=1):
    """
    通过数据文件中的顺序获取学生信息。
    :param num: 数据文件中的顺序
    :return: 学生信息
    """
    students = get_all_students()
    if students == {} or students['students'] == {}:
        logger.warning("配置文件为空！")
        return {'weight': '1', 'id': '000000', 'name': '无结果'}
    num = num - 1
    if students['students'][num]:
        return students['students'][num]
    logger.warning("学生未找到")
    return {'weight': '1', 'id': '000000', 'name': '无结果'}

def get_students_list():
    students = get_all_students()
    list_ = []
    for i in range(1, len(students['students'])+1):
        if students['students'][i-1]['active']:
            list_.append(i)
        i = i + 1
    return list_

def get_students_num():
    """
    获取学生人数。

    :return: 学生人数
    """
    students = get_all_students()
    return len(students['students'])


'''def export2csv():  # WIP
    with open('./students.json', 'r', encoding='utf-8') as json_file:
        students = json.load(json_file)
    with open('./students.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)'''


def excel2json(excel_path='./example.xlsx'):
    """
    从 Excel 文件 (.xls, .xlsx) 导入。

    注意：第一栏要包含 weight, name 和 id. 即相对权重, 姓名和全局学号。

    :param excel_path: Excel 文件路径
    :return: 一个包含所有学生信息的字典
    """
    sheet = pd.read_excel(excel_path)
    students = {}
    list_ = []
    for i in sheet.index.values:
        line = sheet.loc[i, ['weight', 'name', 'id', 'active']].to_dict()
        list_.append(line)
    students['students'] = list_
    return students


def write_conf(students=None):
    """
    写入学生信息。

    :param students:
    :return:
    """
    if students is None:
        return
    data = json.dumps(students, ensure_ascii=False, indent=4)
    with open('./students.json', 'w', encoding='utf-8') as f:
        f.write(data)


def check_config():
    students = {'students': []}
    if not os.path.exists('./students.json'):  # 配置文件不存在
        with open('./students.json', 'w', encoding='utf-8') as f:
            # noinspection PyTypeChecker
            json.dump(students, f, ensure_ascii=False, indent=4)  # 创建空配置文件
    if not os.path.exists('./config.ini'):
        with open('./default_config.json', 'r', encoding='utf-8') as json_file:
            default = json.load(json_file)
        config.read_dict(default)
        with open('./config.ini', 'w', encoding='utf-8') as ini:
            config.write(ini)


def get_all_students():
    with open('./students.json', 'r', encoding='utf-8') as f:
        students = json.load(f)
    return students


def get_weight():
    """
    获取活动学生权重。
    :return: 活动学生权重
    """
    students = get_all_students()
    weight = []
    for student in students['students']:
        if student['active']:
            weight.append(student['weight'])
    return weight

def get_all_weight():
    """
    获取全部学生权重。
    :return: 全部权重
    """
    students = get_all_students()
    weight = []
    for student in students['students']:
        weight.append(student['weight'])
    return weight


def get_ini(section='General', key=''):
    config.read('config.ini')
    with open('./default_config.json', 'r', encoding='utf-8') as f:
        default = json.load(f)
    if section in config and key in config[section]:
        logger.debug(f"已获取配置 {section} -> {key} {config[section][key]}")
        return config[section][key]
    elif section in default and key in default[section]:
        logger.debug(f"已获取默认配置 {section} -> {key} {default[section][key]}")
        return default[section][key]
    return None


config = configparser.ConfigParser()
