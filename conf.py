"""RandPicker 配置文件和数据整理模块。

本模块提供了对学生数据和配置的管理功能，包括：
- 学生信息的获取和查询
- 小组信息的管理
- 配置文件的读写
- 数据导入导出
"""

import configparser
import json
import os.path
from typing import Dict, List, Union, Optional, Any, Tuple

import pandas as pd
from loguru import logger

# 全局配置对象
config = configparser.ConfigParser()

# 常量定义
STUDENTS_FILE = './students.json'
CONFIG_FILE = './config.ini'
DEFAULT_CONFIG_FILE = './default_config.json'
DEFAULT_STUDENT = {'weight': '1', 'id': '000000', 'name': '无结果'}


def get_all_students() -> List[Dict]:
    """获取所有学生信息。
    
    从students.json文件中读取并返回所有学生信息。
    
    Returns:
        List[Dict]: 包含所有学生信息的列表
    """
    try:
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            students = json.load(f)
        return students.get('students', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"读取学生数据失败: {e}")
        return []


def get_student_by(field: str, value: Any) -> Optional[Dict]:
    """通过指定字段查找学生信息。
    
    Args:
        field: 查找依据的字段名，如'id'、'short_id'、'name'等
        value: 字段对应的值
        
    Returns:
        Optional[Dict]: 找到的学生信息，未找到则返回None
    """
    students = get_all_students()
    if not students:
        logger.warning("学生数据为空")
        return DEFAULT_STUDENT.copy()
    
    for student in students:
        if student.get(field) == value:
            return student
    
    return None


def get_with_short_id(num=1) -> Optional[Dict]:
    """通过班级序号获取学生信息。

    Args:
        num: 班级序号
        
    Returns:
        Optional[Dict]: 学生信息，未找到则返回None
    """
    result = get_student_by('short_id', num)
    if result == DEFAULT_STUDENT.copy():
        return {'short_id': '', 'id': '000000', 'name': '无结果'}
    return result


def get_with_id(num=1) -> Optional[Dict]:
    """通过学校全局学号获取学生信息。

    Args:
        num: 全局学号
        
    Returns:
        Optional[Dict]: 学生信息，未找到则返回None
    """
    return get_student_by('id', num)


def get_index_with_name(name: str) -> Optional[int]:
    """通过姓名获取学生在列表中的索引。
    
    Args:
        name: 学生姓名
        
    Returns:
        Optional[int]: 学生在列表中的索引，未找到则返回None
    """
    students = get_all_students()
    if not students:
        return None
    
    for num, student in enumerate(students):
        if student.get('name') == name:
            return num
    
    return None


def get(num=1) -> Dict:
    """通过数据文件中的顺序获取学生信息。
    
    Args:
        num: 数据文件中的顺序（从1开始）
        
    Returns:
        Dict: 学生信息，未找到则返回默认值
    """
    students = get_all_students()
    if not students:
        logger.warning("配置文件为空！")
        return DEFAULT_STUDENT.copy()
    
    try:
        return students[num - 1]
    except IndexError:
        logger.warning(f"学生未找到: 索引{num}超出范围")
        return DEFAULT_STUDENT.copy()


def get_students_list() -> List[int]:
    """获取所有活跃学生的序号列表。
    
    Returns:
        List[int]: 活跃学生的序号列表（从1开始）
    """
    students = get_all_students()
    return [i+1 for i, student in enumerate(students) if student.get('active', False)]


def get_students_name() -> List[str]:
    """获取所有学生的姓名列表。
    
    Returns:
        List[str]: 所有学生的姓名列表
    """
    students = get_all_students()
    return [student.get('name', '') for student in students]


def get_students_num() -> int:
    """获取学生总人数。

    Returns:
        int: 学生总人数
    """
    return len(get_all_students())


def import_from_file(file_path: str) -> List[Dict]:
    """从文件导入学生数据，自动识别Excel(.xls, .xlsx)或CSV格式。

    注意：文件的第一行必须包含 weight, name, id 和 active 列，分别表示相对权重、姓名、全局学号和是否启用。

    Args:
        file_path: 文件路径
        
    Returns:
        List[Dict]: 包含所有学生信息的列表
        
    Raises:
        FileNotFoundError: 文件未找到
        ValueError: 文件格式无效或无法识别
    """
    # 根据文件扩展名自动识别格式
    try:
        if file_path.lower().endswith(('.xls', '.xlsx')):
            sheet = pd.read_excel(file_path)
        elif file_path.lower().endswith('.csv'):
            sheet = pd.read_csv(file_path)
        else:
            # 尝试通过文件内容自动识别
            try:
                sheet = pd.read_excel(file_path)
            except Exception:
                sheet = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件未找到: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"文件为空或无效: {file_path}")
    except Exception as e:
        raise ValueError(f"无法识别的文件格式: {file_path}, 错误: {e}")

    # 检查必要的列是否存在
    required_columns = ['weight', 'name', 'id', 'active']
    missing_columns = [col for col in required_columns if col not in sheet.columns]
    if missing_columns:
        raise ValueError(f"文件缺少必要的列: {', '.join(missing_columns)}")

    # 转换为字典列表
    return [row[required_columns].to_dict() for _, row in sheet.iterrows()]


def excel2json(file_path='./example.xlsx') -> List[Dict]:
    """从Excel文件导入学生数据。

    注意：第一栏要包含 weight, name, id 和 active 列。

    Args:
        file_path: Excel文件路径
        
    Returns:
        List[Dict]: 包含所有学生信息的列表
    """
    return import_from_file(file_path)


def csv2json(csv_path='./example.csv') -> List[Dict]:
    """从CSV文件导入学生数据。

    注意：第一栏要包含 weight, name, id 和 active 列。

    Args:
        csv_path: CSV文件路径
        
    Returns:
        List[Dict]: 包含所有学生信息的列表
    """
    return import_from_file(csv_path)


def write_conf(students=None, groups=None) -> None:
    """写入学生和小组信息到配置文件。

    Args:
        students: 学生信息列表，为None则保留原有数据
        groups: 小组信息列表，为None则保留原有数据
    """
    try:
        # 读取现有数据
        try:
            with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            old_data = {'students': [], 'groups': []}
        
        # 更新数据
        new_data = {
            'students': students if students is not None else old_data.get('students', []),
            'groups': groups if groups is not None else old_data.get('groups', [])
        }
        
        # 写入文件
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
            
        logger.debug("配置文件更新成功")
    except Exception as e:
        logger.error(f"写入配置文件失败: {e}")


def check_config() -> None:
    """检查并初始化配置文件。
    
    如果配置文件不存在，则创建默认配置文件。
    """
    # 检查学生数据文件
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'students': [], 'groups': []}, f, ensure_ascii=False, indent=4)
            logger.info(f"已创建空的学生数据文件: {STUDENTS_FILE}")
    
    # 检查配置文件
    if not os.path.exists(CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as json_file:
                default = json.load(json_file)
            config.read_dict(default)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as ini:
                config.write(ini)
            logger.info(f"已从默认配置创建配置文件: {CONFIG_FILE}")
        except Exception as e:
            logger.error(f"创建配置文件失败: {e}")


def get_weight() -> List[Union[int, float, str]]:
    """获取活动学生的权重列表。
    
    Returns:
        List[Union[int, float, str]]: 活动学生的权重列表
    """
    students = get_all_students()
    return [student.get('weight', 1) for student in students if student.get('active', False)]


def get_all_weight() -> List[Union[int, float, str]]:
    """获取所有学生的权重列表。
    
    Returns:
        List[Union[int, float, str]]: 所有学生的权重列表
    """
    students = get_all_students()
    return [student.get('weight', 1) for student in students]


def get_some_weight(stu_indices: List[int]) -> List[Union[int, float, str]]:
    """获取指定学生的权重列表。
    
    Args:
        stu_indices: 学生索引列表（从1开始）
        
    Returns:
        List[Union[int, float, str]]: 指定学生的权重列表
    """
    students = get_all_students()
    result = []
    
    for idx in stu_indices:
        try:
            student = students[idx - 1]
            if student.get('active', False):
                result.append(student.get('weight', 1))
        except IndexError:
            logger.warning(f"学生索引超出范围: {idx}")
    
    return result


def get_all_group() -> List[Dict]:
    """获取所有小组信息。
    
    Returns:
        List[Dict]: 所有小组信息的列表
    """
    try:
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('groups', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"读取小组数据失败: {e}")
        return []


def get_group_len() -> int:
    """获取小组数量。
    
    Returns:
        int: 小组数量
    """
    return len(get_all_group())


def get_group(num: int) -> Dict:
    """获取指定索引的小组信息。
    
    Args:
        num: 小组索引
        
    Returns:
        Dict: 小组信息
    """
    groups = get_all_group()
    try:
        return groups[num]
    except IndexError:
        logger.warning(f"小组索引超出范围: {num}")
        return {}


def get_group_num(name: str = '测试1') -> Optional[int]:
    """通过小组名称获取小组索引。
    
    Args:
        name: 小组名称
        
    Returns:
        Optional[int]: 小组索引，未找到则返回None
    """
    groups = get_all_group()
    for index, group in enumerate(groups):
        if group.get('name') == name:
            return index
    return None


def get_students_name_in_group(group: Union[int, Dict]) -> List[str]:
    """获取小组中所有学生的姓名列表。
    
    Args:
        group: 小组索引或小组信息字典
        
    Returns:
        List[str]: 小组中所有学生的姓名列表
    """
    if isinstance(group, int):
        group = get_group(group)
    
    if not group or 'stu' not in group:
        return []
    
    return [get(student + 1).get('name', '') for student in group.get('stu', [])]


def get_students_in_group(group: Union[int, Dict]) -> List[int]:
    """获取小组中所有学生的索引列表。
    
    Args:
        group: 小组索引或小组信息字典
        
    Returns:
        List[int]: 小组中所有学生的索引列表（从1开始）
    """
    if isinstance(group, int):
        group = get_group(group)
    
    if not group or 'stu' not in group:
        return []
    
    return [student + 1 for student in group.get('stu', [])]


def get_ini(section='General', key='') -> Optional[str]:
    """获取配置项的值。
    
    先从配置文件中查找，如果未找到则从默认配置中查找。
    
    Args:
        section: 配置节名称
        key: 配置项名称
        
    Returns:
        Optional[str]: 配置项的值，未找到则返回None
    """
    config.read(CONFIG_FILE)
    
    # 尝试从配置文件中获取
    if section in config and key in config[section]:
        value = config[section][key]
        logger.debug(f"已获取配置 {section} -> {key}。它的值是 {value}。")
        return value
    
    # 尝试从默认配置中获取
    try:
        with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
            default = json.load(f)
        
        if section in default and key in default[section]:
            value = default[section][key]
            logger.debug(f"已获取默认配置 {section} -> {key}。它的值是 {value}。")
            return value
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"读取默认配置失败: {e}")
    
    return None


def write_ini(*args, file_path=CONFIG_FILE) -> None:
    """写入或更新指定INI文件的内容。

    Args:
        *args: 成对的Section、Key和Value值
        file_path: INI文件的路径，默认为config.ini
        
    Raises:
        ValueError: 参数数量不是3的倍数
    """
    if len(args) % 3 != 0:
        raise ValueError("必须是成对的section, key, value")

    # 读取现有文件
    config.read(file_path, encoding='utf-8')

    # 准备并更新数据
    for i in range(0, len(args), 3):
        section, key, value = args[i], args[i + 1], args[i + 2]
        
        if not config.has_section(section):
            config.add_section(section)
        
        config.set(section, key, str(value))

    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        logger.debug(f"配置文件 {file_path} 更新成功")
    except Exception as e:
        logger.error(f"写入配置文件 {file_path} 失败: {e}")


def get_group_weight(group_index: int) -> Union[int, float]:
    """获取小组权重。
    
    Args:
        group_index: 小组索引
        
    Returns:
        Union[int, float]: 小组权重，默认为1
    """
    group = get_group(group_index)
    return group.get('weight', 1) if group else 1


def get_all_group_weights() -> List[Union[int, float]]:
    """获取所有小组的权重列表。
    
    Returns:
        List[Union[int, float]]: 所有小组的权重列表
    """
    groups = get_all_group()
    return [group.get('weight', 1) for group in groups]


def set_group_weight(group_index: int, weight: Union[int, float]) -> bool:
    """设置小组权重。
    
    Args:
        group_index: 小组索引
        weight: 权重值
        
    Returns:
        bool: 是否设置成功
    """
    try:
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'groups' not in data or len(data['groups']) <= group_index:
            logger.warning(f"小组索引超出范围: {group_index}")
            return False
        
        data['groups'][group_index]['weight'] = weight
        
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        logger.debug(f"小组 {group_index} 权重已更新为 {weight}")
        return True
    except Exception as e:
        logger.error(f"设置小组权重失败: {e}")
        return False
