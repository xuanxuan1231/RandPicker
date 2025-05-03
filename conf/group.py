import json

from . import stu

# region 通用方法
def get_all():
    with open('./students.json', 'r', encoding='utf-8') as f:
        students = json.load(f)
    return students['groups']

groups = get_all()

def _refresh():
    global groups
    groups = get_all()
# endregion


# region 小组
def get_single(index: int) -> dict:
    """
    获取单个小组。

    :param index: 小组索引
    :type index: int
    """
    _refresh()
    global groups
    return groups[index]


def get_index(name: str = '测试1'):
    """
    从小组名称获取索引。

    :param name: 小组名称
    :type name: str
    """
    _refresh()
    global groups
    for index, group in enumerate(groups):
        if group['name'] == name:
            return index
    return


def get_stu_name(group: int | dict):
    """
    获取小组中的所有学生的，姓名的列表。

    :param group: 小组索引或小组的全部信息
    :type group: int | dict
    """
    if isinstance(group, int):
        group = get_single(group)
    list_ = []
    for student in group['stu']:
        list_.append(stu.get_single(student)['name'])
    return list_


def get_stu_index(group: int | dict):
    """
    获取小组中的所有学生的，索引的列表。

    :param group: 小组索引或小组的全部信息
    :type group: int | dict
    """
    if isinstance(group, int):
        group = get_single(group)
    list_ = []
    for student in group['stu']:
        list_.append(student)
    return list_
# endregion