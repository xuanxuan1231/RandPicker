"""
对配置文件进行操作。

"""

import json
import os

from configparser import ConfigParser
from loguru import logger

_config = ConfigParser()

def check_config():
    if not os.path.exists('./config.ini'):
        with open('./default_config.json', 'r', encoding='utf-8') as json_file:
            default = json.load(json_file)
        _config.read_dict(default)
        with open('./config.ini', 'w', encoding='utf-8') as ini:
            # noinspection PyTypeChecker
            _config.write(ini)

check_config()

def get(section: str = 'General', key: str = '') -> str:
    """
    获取配置文件。

    :param section: 配置文件的 Section
    :type section: str
    :param key: 配置文件 Section 中的键
    :type key: str
    """
    _config.read('config.ini', encoding='utf-8')

    with open('./default_config.json', 'r', encoding='utf-8') as f:
        default = json.load(f)
    
    if section in _config and key in _config[section]:
        logger.debug(f"从配置中获取到 {section} -> {key} = {_config[section][key]}。")
        return _config[section][key]
    elif section in default and key in default[section]:
        logger.debug(f"从默认配置获取到 {section} -> {key} = {default[section][key]}。")
        write(section, key, default[section][key])
        logger.debug(f"在配置文件中加入 {section} -> {key} = {default[section][key]}。")
        return default[section][key]
    logger.error(f"没有获取到 {section} -> {key}。返回 NoneType。")
    return None

def write(*args):
    """
    写入或更新配置文件。

    :param args: 成对的 Section 和 Key 值，后面跟着对应的 Value 值。
    """
    if len(args) % 3 != 0:
        raise ValueError("必须是成对的 section, key, value。")

    # 读取现有文件（如果存在）
    _config.read('config.ini', encoding='utf-8')

    # 准备数据
    sections_data = {}
    for i in range(0, len(args), 3):
        section, key, value = args[i], args[i + 1], args[i + 2]
        if section not in sections_data:
            sections_data[section] = {}
        sections_data[section][key] = value

    # 更新/添加section和对应的键值对
    for section, data in sections_data.items():
        if not _config.has_section(section):
            _config.add_section(section)
        for key, value in data.items():
            _config.set(section, key, str(value))

    # 将更改写回文件
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        _config.write(configfile)
