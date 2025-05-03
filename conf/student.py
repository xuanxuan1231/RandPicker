import json

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

# region 权重


# endregion
