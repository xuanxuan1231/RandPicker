"""RandPicker 配置管理。

此模块提供配置文件的读写和管理功能。
"""
import json
import os
from loguru import logger

import conf


def load_config(config_type='ui'):
    """加载配置
    
    :param config_type: 配置类型，可选值：'ui', 'student', 'group'
    :return: 配置字典
    """
    if config_type == 'ui':
        # 从ini配置文件加载UI设置
        return {
            'avatar_size': int(conf.ini.get('UI', 'avatar_size')),
            'edge_hide': conf.ini.get('UI', 'edge_hide') == 'true',
            'edge_distance': int(conf.ini.get('UI', 'edge_distance')),
            'hidden_width': int(conf.ini.get('UI', 'hidden_width')),
            'avatar': conf.ini.get('UI', 'avatar') == 'true',
            'scale': float(conf.ini.get('General', 'scale')),
            'theme': int(conf.ini.get('General', 'theme')),
            'elastic_animation': conf.ini.get('UI', 'elastic_animation') == 'true',
            'color': conf.ini.get('Color', 'dark' if conf.ini.get('General', 'theme') == '1' else 'light')
        }
    elif config_type == 'student':
        # 加载学生配置
        return conf.stu.get_all()
    elif config_type == 'group':
        # 加载分组配置
        return conf.group.get_all()
    else:
        logger.error(f"未知的配置类型: {config_type}")
        return {}


def save_config(config_data, config_type='ui'):
    """保存配置
    
    :param config_data: 配置数据
    :param config_type: 配置类型，可选值：'ui', 'student', 'group'
    :return: 是否保存成功
    """
    try:
        if config_type == 'ui':
            # 保存UI设置到ini配置文件
            conf.ini.write(
                'UI', 'avatar_size', str(config_data.get('avatar_size', 100)),
                'UI', 'edge_hide', 'true' if config_data.get('edge_hide', False) else 'false',
                'UI', 'edge_distance', str(config_data.get('edge_distance', 20)),
                'UI', 'hidden_width', str(config_data.get('hidden_width', 20)),
                'UI', 'avatar', 'true' if config_data.get('avatar', True) else 'false',
                'UI', 'elastic_animation', 'true' if config_data.get('elastic_animation', True) else 'false',
                'General', 'scale', str(config_data.get('scale', 1.0)),
                'General', 'theme', str(config_data.get('theme', 2)),
                'Color', 'dark' if config_data.get('theme', 2) == 1 else 'light', config_data.get('color', '#009faa')
            )
            logger.info("UI配置已保存")
        elif config_type == 'student':
            # 保存学生配置
            conf.write_conf(students=config_data)
            logger.info("学生配置已保存")
        elif config_type == 'group':
            # 保存分组配置
            conf.write_conf(groups=config_data)
            logger.info("分组配置已保存")
        else:
            logger.error(f"未知的配置类型: {config_type}")
            return False
        return True
    except Exception as e:
        logger.error(f"保存配置失败: {str(e)}")
        return False


def get_default_config(config_type='ui'):
    """获取默认配置
    
    :param config_type: 配置类型，可选值：'ui', 'student', 'group'
    :return: 默认配置字典
    """
    if config_type == 'ui':
        # 默认UI设置
        return {
            'avatar_size': 100,
            'edge_hide': False,
            'edge_distance': 20,
            'hidden_width': 20,
            'avatar': True,
            'scale': 1.0,
            'theme': 2,  # 跟随系统
            'elastic_animation': True,
            'color': '#009faa'
        }
    elif config_type == 'student':
        # 默认学生配置
        if os.path.exists('./default_students.json'):
            with open('./default_students.json', 'r', encoding='utf-8') as f:
                return json.load(f).get('students', [])
        return []
    elif config_type == 'group':
        # 默认分组配置
        return []
    else:
        logger.error(f"未知的配置类型: {config_type}")
        return {}