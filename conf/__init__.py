import json

from configparser import ConfigParser

from . import ini, group, stu, imp

def write_conf(students: dict | None, groups: dict | None):
    """
    写入学生信息。

    :param students: 要写入的全部学生信息 (如有)
    :param groups: 要写入的全部小组信息 (如有)
    """
    with open('./students.json', 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    new_data = {}

    if students is None:
        new_data['students'] = old_data['students']
    else:
        new_data['students'] = students

    if groups is None:
        new_data['groups'] = old_data['groups']
    else:
        new_data['groups'] = groups

    data = json.dumps(new_data, ensure_ascii=False, indent=4)
    with open('./students.json', 'w', encoding='utf-8') as f:
        f.write(data)


def check_config():
    ini.check_config()
    stu.check_config()