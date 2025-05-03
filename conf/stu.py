import json
import os

from loguru import logger

# region 检查配置文件
def check_config():
    if not os.path.exists('./students.json'):  # 配置文件不存在
        with open('./default_students.json', 'r', encoding='utf-8') as default:
            students = json.load(default)
        with open('./students.json', 'w', encoding='utf-8') as f:
            # noinspection PyTypeChecker
            json.dump(students, f, ensure_ascii=False, indent=4)  # 创建空配置文件
# endregion

check_config()

# region 通用方法
def get_all() -> list:
    with open('students.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['students']

students = get_all()

def _refresh():
    global students
    students = get_all()
# endregion


# region 学生
def get_all_name() -> list:
    """
    获取所有学生的姓名。
    """
    _refresh()
    global students
    list_ = []
    for student in students:
        list_.append(student['name'])
    return list_

def get_active_index() -> list:
    """
    获取所有活动学生的索引。从 0 开始。
    """
    _refresh()
    global students
    list_ = []
    for i in range(0, len(students)):
        if students[i]['active']:
            list_.append(i)
    return list_

def get_single(index: int = 0) -> dict:
    """
    从索引获取单个学生的信息。

    :param index: 索引
    :type index: int
    """
    _refresh()
    global students
    if students == {}:
        logger.warning("配置文件为空！")
        return {'weight': '1', 'id': '000000', 'name': '无结果', 'active': True}
    if students[index]:
        return students[index]
    logger.warning("学生未找到")
    return {'weight': '1', 'id': '000000', 'name': '无结果', 'active': True}

def get_index_4name(name: str = '') -> int:
    """
    从姓名获取单个学生的索引。

    :param name: 姓名
    :type name: str
    """
    _refresh()
    global students
    if students == {}:
        return None
    for num, student in enumerate(students):
        if student['name'] == name:
            return num
    return None
# endregion

# region 权重
def get_all_weight():
    """
    获取全部学生权重。
    :return: 全部权重
    """
    _refresh()
    global students
    weight = []
    for student in students:
        # 如果学生记录中没有weight字段，则使用默认权重1
        weight.append(student.get('weight', 1))
    return weight

def get_weight(stu: list = None) -> list:
    """
    获取给定索引列表中的，各个权重。

    :param stu: 索引列表
    :type stu: list
    """
    
    result = []
    for student in stu:
        if students[student]:
            result.append(students[student]['weight'])
    return result
# endregion
