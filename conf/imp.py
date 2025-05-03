import json

import pandas as pd

def excel2json(file_path: str = './example.xlsx') -> list:
    """
    从 Excel 文件导入学生数据。

    注意：第一栏要包含 weight, name, id 和 active. 即相对权重, 姓名, 全局学号和是否启用。

    :param file_path: 文件路径
    :return: 一个包含所有学生信息的列表
    """
    sheet = pd.read_excel(file_path)
    list_ = []
    for i in sheet.index.values:
        line = sheet.loc[i, ['weight', 'name', 'id', 'active']].to_dict()
        list_.append(line)
    return list_


def csv2json(csv_path: str = './example.csv') -> list:
    """
    从 CSV 文件导入。

    注意：第一栏要包含 weight, name, id 和 active. 即相对权重, 姓名, 全局学号和是否启用。

    :param csv_path: CSV 文件路径
    :return: 一个包含所有学生信息的列表
    """
    sheet = pd.read_csv(csv_path)
    list_ = []
    for i in sheet.index.values:
        line = sheet.loc[i, ['weight', 'name', 'id', 'active']].to_dict()
        list_.append(line)
    return list_