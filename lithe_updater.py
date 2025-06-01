"""RandPicker LitheNum 版本更新工具

此模块基于LitheNum.md中定义的版本策略，提供不同版本通道的更新检查和下载功能。
"""
import sys
import os
import re
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

import requests
from packaging.version import Version
from loguru import logger
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import InfoBar, InfoBarPosition, ProgressBar

import conf


class VersionChannel(Enum):
    """版本通道枚举"""
    MAIN = 'M'      # 主要版本
    LTS = 'L'       # 长期支持版本
    TEST = 'T'      # 测试版本
    DEV = 'D'       # 开发者版本
    EXP = 'E'       # 实验性版本
    
    @classmethod
    def from_index(cls, idx: int) -> 'VersionChannel':
        """从索引获取版本通道"""
        mapping = {
            0: cls.MAIN,
            1: cls.LTS,
            2: cls.TEST,
            3: cls.DEV,
            4: cls.EXP
        }
        return mapping.get(idx, cls.LTS)  # 默认返回LTS
    
    @classmethod
    def to_index(cls, channel: 'VersionChannel') -> int:
        """将版本通道转换为索引"""
        mapping = {
            cls.MAIN: 0,
            cls.LTS: 1,
            cls.TEST: 2,
            cls.DEV: 3,
            cls.EXP: 4
        }
        return mapping.get(channel, 1)  # 默认返回LTS索引
    
    @classmethod
    def to_display_name(cls, channel: 'VersionChannel') -> str:
        """获取版本通道的显示名称"""
        mapping = {
            cls.MAIN: 'M 主版本(Main)',
            cls.LTS: 'L 稳定版(Long time support)',
            cls.TEST: 'T 测试版(Test)',
            cls.DEV: 'D 开发版(Developer)',
            cls.EXP: 'E 实验版(Experimental)'
        }
        return mapping.get(channel, 'L 稳定版(Long time support)')
    
    @classmethod
    def to_api_name(cls, channel: 'VersionChannel') -> str:
        """获取版本通道的API名称"""
        mapping = {
            cls.MAIN: 'main',
            cls.LTS: 'lts',
            cls.TEST: 'test',
            cls.DEV: 'dev',
            cls.EXP: 'exp'
        }
        return mapping.get(channel, 'lts')


@dataclass
class LitheVersion:
    """LitheNum版本"""
    channel: VersionChannel  # 版本通道
    major: int               # 主版本号
    minor: int               # 次版本号
    build: Optional[int] = None  # 构建号
    
    @classmethod
    def parse(cls, version_str: str) -> Optional['LitheVersion']:
        """解析版本字符串"""
        # 移除v前缀
        if version_str.startswith('v'):
            version_str = version_str[1:]
        
        # 尝试匹配LitheNum格式
        pattern = r'^([MLTED])\.([0-9]+)\.([0-9]+)(?:\.([0-9]+))?$'
        match = re.match(pattern, version_str)
        
        if match:
            channel_str, major_str, minor_str, build_str = match.groups()
            
            # 映射通道字符串到枚举
            channel_map = {
                'M': VersionChannel.MAIN,
                'L': VersionChannel.LTS,
                'T': VersionChannel.TEST,
                'D': VersionChannel.DEV,
                'E': VersionChannel.EXP
            }
            
            channel = channel_map.get(channel_str, VersionChannel.LTS)
            major = int(major_str)
            minor = int(minor_str)
            build = int(build_str) if build_str else None
            
            return cls(channel, major, minor, build)
        
        # 尝试匹配标准版本格式
        try:
            v = Version(version_str)
            return cls(
                VersionChannel.LTS,  # 默认为LTS
                v.major,
                v.minor,
                v.micro if v.micro != 0 else None
            )
        except:
            return None
    
    def __str__(self) -> str:
        """转换为字符串"""
        if self.build is not None:
            return f"{self.channel.value}.{self.major}.{self.minor}.{self.build}"
        return f"{self.channel.value}.{self.major}.{self.minor}"
    
    def to_version(self) -> Version:
        """转换为packaging.version.Version对象"""
        if self.build is not None:
            return Version(f"{self.major}.{self.minor}.{self.build}")
        return Version(f"{self.major}.{self.minor}.0")
    
    def __lt__(self, other):
        """小于比较"""
        if not isinstance(other, LitheVersion):
            return NotImplemented
        
        # 如果通道不同，无法直接比较版本
        if self.channel != other.channel:
            return False
        
        # 比较版本号
        return self.to_version() < other.to_version()
    
    def __eq__(self, other):
        """等于比较"""
        if not isinstance(other, LitheVersion):
            return NotImplemented
        
        # 通道必须相同
        if self.channel != other.channel:
            return False
        
        # 比较版本号
        return self.to_version() == other.to_version()


# 当前应用版本
APP_VERSION = LitheVersion.parse('L.1.5.1')  # 默认版本


def get_current_version() -> LitheVersion:
    """获取当前应用版本"""
    return APP_VERSION


def get_current_channel() -> VersionChannel:
    """获取当前更新通道设置"""
    try:
        channel_idx = int(conf.ini.get('Update', 'channel', fallback='1'))
        return VersionChannel.from_index(channel_idx)
    except Exception:
        logger.error("获取更新通道失败，使用默认通道LTS")
        return VersionChannel.LTS


def check_update(origin: int = 0) -> Dict:
    """检查更新
    
    :param origin: 更新源。0=GitHub, 1=OSS
    :return: 包含最新版本信息的字典
    """
    logger.info('开始检查更新。')
    result = {}
    
    # 获取当前版本和通道
    current_version = get_current_version()
    channel = get_current_channel()
    api_channel = VersionChannel.to_api_name(channel)
    
    logger.info(f'当前版本: {current_version}, 使用更新通道: {VersionChannel.to_display_name(channel)}')
    
    # 构建API URL
    repo = 'xuanxuan1231/RandPicker'
    if origin == 1:  # OSS源
        manifest_url = f'https://oss.may.pp.ua/RandPicker/{api_channel}/latest.json'
    else:  # GitHub源
        if api_channel == 'main':
            manifest_url = f'https://api.github.com/repos/{repo}/releases/latest'
        else:
            manifest_url = f'https://api.github.com/repos/{repo}/releases/tags/{api_channel}'
    
    logger.info(f'请求URL: {manifest_url}')
    
    try:
        response = requests.get(manifest_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # 解析版本号
        tag_name = data.get('tag_name')
        latest_version = LitheVersion.parse(tag_name)
        
        if not latest_version:
            logger.error(f'无法解析版本号: {tag_name}')
            return {
                'version': str(current_version),
                'is_latest': True,
                'download_url': None,
                'channel': VersionChannel.to_display_name(channel)
            }
        
        # 检查是否有更新
        if latest_version.channel == channel and latest_version > current_version:
            is_latest = False
            logger.info(f'发现新版本 {latest_version}。')
        else:
            is_latest = True
            logger.info('当前版本是最新的。')
        
        # 获取下载URL
        download_url = None
        if not is_latest and 'assets' in data and data['assets']:
            for asset in data['assets']:
                if asset.get('name', '').endswith('.zip') or asset.get('name', '').endswith('.exe'):
                    download_url = asset.get('browser_download_url')
                    break
        
        result = {
            'version': str(latest_version),
            'is_latest': is_latest,
            'download_url': download_url,
            'channel': VersionChannel.to_display_name(channel)
        }
        
    except Exception as e:
        logger.error(f'检查更新时发生错误: {e}')
        result = {
            'version': str(current_version),
            'is_latest': True,
            'download_url': None,
            'channel': VersionChannel.to_display_name(channel)
        }
    
    return result


def download_update(url: str, save_path: str, parent: QWidget = None) -> bool:
    """下载更新包
    
    :param url: 下载URL
    :param save_path: 保存路径
    :param parent: 父窗口，用于显示进度条
    :return: 是否下载成功
    """
    try:
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        total = int(resp.headers.get('content-length', 0))
        chunk_size = 8192
        downloaded = 0
        
        with open(save_path, 'wb') as f:
            pb = None
            if parent:
                pb = ProgressBar(parent)
                pb.setRange(0, 100)
                pb.setValue(0)
                parent.layout().addWidget(pb)
            
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if pb and total:
                        pb.setValue(int(downloaded / total * 100))
            
            if pb:
                pb.setValue(100)
        
        logger.info(f'更新包已下载到: {save_path}')
        return True
    
    except Exception as e:
        logger.error(f'下载更新包失败: {e}')
        if parent:
            InfoBar.error(
                title='下载失败',
                content=str(e),
                parent=parent,
                position=InfoBarPosition.TOP
            )
        return False


def update_app(parent: QWidget = None) -> bool:
    """更新应用程序
    
    :param parent: 父窗口
    :return: 是否成功启动更新
    """
    logger.info('开始更新应用程序。')
    
    # 检查更新
    origin = int(conf.ini.get('Update', 'app', fallback='0'))
    update_info = check_update(origin)
    
    if update_info['is_latest']:
        logger.info('当前已是最新版本，无需更新。')
        if parent:
            InfoBar.success(
                title='已是最新版本',
                content='当前已是最新版本，无需更新。',
                parent=parent,
                position=InfoBarPosition.TOP
            )
        return False
    
    # 获取下载URL
    url = update_info.get('download_url')
    if not url:
        logger.error('未找到可用的更新包下载链接。')
        if parent:
            InfoBar.error(
                title='更新失败',
                content='未找到可用的更新包下载链接。',
                parent=parent,
                position=InfoBarPosition.TOP
            )
        return False
    
    # 下载更新包
    filename = url.split('/')[-1]
    save_path = os.path.join(os.path.expanduser('~'), 'Downloads', filename)
    
    if download_update(url, save_path, parent):
        logger.info(f'更新包已下载到: {save_path}')
        
        # 根据平台执行不同的更新操作
        if sys.platform == 'win32':
            # Windows平台使用更新助理
            try:
                import subprocess
                subprocess.Popen(['Updater.exe', save_path])
                return True
            except Exception as e:
                logger.error(f'启动更新助理失败: {e}')
                if parent:
                    InfoBar.error(
                        title='更新失败',
                        content=f'启动更新助理失败: {e}',
                        parent=parent,
                        position=InfoBarPosition.TOP
                    )
                return False
        else:
            # 其他平台提示手动更新
            if parent:
                InfoBar.success(
                    title='下载完成',
                    content=f'更新包已下载到: {save_path}\n请手动解压并替换程序文件。',
                    parent=parent,
                    position=InfoBarPosition.TOP,
                    duration=5000
                )
            return True
    
    return False


def get_channel_list() -> List[str]:
    """获取所有版本通道的显示名称列表"""
    return [
        VersionChannel.to_display_name(VersionChannel.MAIN),
        VersionChannel.to_display_name(VersionChannel.LTS),
        VersionChannel.to_display_name(VersionChannel.TEST),
        VersionChannel.to_display_name(VersionChannel.DEV),
        VersionChannel.to_display_name(VersionChannel.EXP)
    ]


def set_channel(channel_idx: int) -> None:
    """设置更新通道
    
    :param channel_idx: 通道索引
    """
    conf.ini.write('Update', 'channel', str(channel_idx))
    logger.info(f'已设置更新通道为: {VersionChannel.to_display_name(VersionChannel.from_index(channel_idx))}')