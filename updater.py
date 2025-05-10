"""RandPicker 更新模块。
提供应用内更新功能，包括版本检查、下载和安装更新。
"""

import json
import os
import platform
import re
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from threading import Thread

import requests
from PyQt6.QtCore import QObject, pyqtSignal, QUrl, Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import Dialog, PrimaryPushButton, PushButton, MessageBox, StateToolTip, InfoBar, InfoBarPosition
from loguru import logger

# 当前版本号
CURRENT_VERSION = "1.0.0"

# GitHub 仓库信息
REPO_OWNER = "xuanxuan1231"
REPO_NAME = "RandPicker"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"


class Updater(QObject):
    """更新管理器类，处理检查更新、下载和安装过程"""
    # 定义信号
    update_available = pyqtSignal(str, str)  # 有更新可用(版本号, 更新说明)
    update_not_available = pyqtSignal()  # 没有可用更新
    download_progress = pyqtSignal(int, int)  # 下载进度(当前, 总大小)
    download_complete = pyqtSignal(str)  # 下载完成(文件路径)
    download_error = pyqtSignal(str)  # 下载错误(错误信息)
    install_complete = pyqtSignal()  # 安装完成
    install_error = pyqtSignal(str)  # 安装错误(错误信息)
    check_error = pyqtSignal(str)  # 检查更新错误(错误信息)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.latest_version = None
        self.download_url = None
        self.release_notes = None
        self.temp_dir = None
        self.download_path = None
        self.state_tooltip = None

    def check_for_updates(self, silent=False):
        """检查更新
        
        Args:
            silent: 是否静默检查，不显示无更新提示
        """
        try:
            logger.info(f"检查更新，当前版本: {CURRENT_VERSION}")
            
            # 创建线程执行检查
            thread = Thread(target=self._check_update_thread, args=(silent,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            logger.error(f"启动检查更新线程失败: {str(e)}")
            self.check_error.emit(f"检查更新失败: {str(e)}")

    def _check_update_thread(self, silent):
        """检查更新的线程函数"""
        try:
            # 获取最新版本信息
            try:
                response = requests.get(API_URL, timeout=15)
                response.raise_for_status()
                release_data = response.json()
            except requests.exceptions.Timeout:
                raise Exception("连接超时，请检查网络连接后重试")
            except requests.exceptions.ConnectionError:
                raise Exception("网络连接错误，请检查网络连接后重试")
            except requests.exceptions.HTTPError as e:
                raise Exception(f"HTTP错误: {e}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"请求错误: {e}")
            except json.JSONDecodeError:
                raise Exception("无法解析服务器响应，请稍后重试")
            
            # 提取版本号（去除v前缀）
            latest_version = release_data['tag_name'].lstrip('v')
            self.latest_version = latest_version
            self.release_notes = release_data['body']
            
            # 获取下载URL
            for asset in release_data['assets']:
                if asset['name'].endswith('.zip'):
                    self.download_url = asset['browser_download_url']
                    break
            
            # 比较版本号
            if self._compare_versions(latest_version, CURRENT_VERSION) > 0:
                logger.info(f"发现新版本: {latest_version}")
                self.update_available.emit(latest_version, self.release_notes)
            else:
                logger.info("当前已是最新版本")
                if not silent:
                    self.update_not_available.emit()
                    
        except Exception as e:
            logger.error(f"检查更新失败: {str(e)}")
            self.check_error.emit(f"检查更新失败: {str(e)}")

    def download_update(self):
        """下载更新"""
        if not self.download_url:
            self.download_error.emit("下载链接不可用")
            return
            
        try:
            # 创建临时目录
            self.temp_dir = tempfile.mkdtemp(prefix="randpicker_update_")
            self.download_path = os.path.join(self.temp_dir, f"RandPicker_{self.latest_version}.zip")
            
            # 显示下载状态提示
            self.state_tooltip = StateToolTip("正在下载更新", "请稍候...", QApplication.activeWindow())
            self.state_tooltip.show()
            
            # 创建线程执行下载
            thread = Thread(target=self._download_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            logger.error(f"启动下载线程失败: {str(e)}")
            self.download_error.emit(f"下载更新失败: {str(e)}")
            if self.state_tooltip:
                self.state_tooltip.setState(False)
                self.state_tooltip = None

    def _download_thread(self):
        """下载更新的线程函数"""
        try:
            # 下载文件
            try:
                response = requests.get(self.download_url, stream=True, timeout=30)
                response.raise_for_status()
            except requests.exceptions.Timeout:
                raise Exception("下载超时，请检查网络连接后重试")
            except requests.exceptions.ConnectionError:
                raise Exception("网络连接错误，请检查网络连接后重试")
            except requests.exceptions.HTTPError as e:
                raise Exception(f"HTTP错误: {e}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"请求错误: {e}")
            
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            if total_size == 0:
                logger.warning("无法获取文件大小信息")
            downloaded_size = 0
            
            # 写入文件
            with open(self.download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        # 更新进度
                        self.download_progress.emit(downloaded_size, total_size)
                        
                        # 更新状态提示
                        if self.state_tooltip and total_size > 0:
                            progress = int(downloaded_size * 100 / total_size)
                            self.state_tooltip.setContent(f"下载进度: {progress}%")
            
            logger.info(f"更新包下载完成: {self.download_path}")
            
            # 更新状态提示
            if self.state_tooltip:
                self.state_tooltip.setContent("下载完成")
                self.state_tooltip.setState(True)
                self.state_tooltip = None
                
            # 发出下载完成信号
            self.download_complete.emit(self.download_path)
            
        except Exception as e:
            logger.error(f"下载更新失败: {str(e)}")
            self.download_error.emit(f"下载更新失败: {str(e)}")
            if self.state_tooltip:
                self.state_tooltip.setState(False)
                self.state_tooltip = None

    def install_update(self, download_path):
        """安装更新
        
        Args:
            download_path: 下载的更新包路径
        """
        try:
            # 显示安装状态提示
            self.state_tooltip = StateToolTip("正在安装更新", "请稍候...", QApplication.activeWindow())
            self.state_tooltip.show()
            
            # 创建线程执行安装
            thread = Thread(target=self._install_thread, args=(download_path,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            logger.error(f"启动安装线程失败: {str(e)}")
            self.install_error.emit(f"安装更新失败: {str(e)}")
            if self.state_tooltip:
                self.state_tooltip.setState(False)
                self.state_tooltip = None

    def _install_thread(self, download_path):
        """安装更新的线程函数"""
        try:
            # 检查文件是否存在
            if not os.path.exists(download_path):
                raise Exception("更新包文件不存在，请重新下载")
                
            # 检查文件大小
            file_size = os.path.getsize(download_path)
            if file_size < 1024:  # 小于1KB的文件可能是错误的
                raise Exception("更新包文件不完整，请重新下载")
                
            # 解压更新包
            extract_dir = os.path.join(self.temp_dir, "extract")
            os.makedirs(extract_dir, exist_ok=True)
            
            try:
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    # 检查zip文件完整性
                    if zip_ref.testzip() is not None:
                        raise Exception("更新包文件损坏，请重新下载")
                    zip_ref.extractall(extract_dir)
            except zipfile.BadZipFile:
                raise Exception("更新包格式错误，请重新下载")
            except Exception as e:
                raise Exception(f"解压更新包失败: {str(e)}")
            
            # 获取应用目录
            app_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
            
            # 更新文件（排除特定文件和目录）
            self._update_files(extract_dir, app_dir)
            
            logger.info("更新安装完成")
            
            # 更新状态提示
            if self.state_tooltip:
                self.state_tooltip.setContent("安装完成，即将重启应用")
                self.state_tooltip.setState(True)
                self.state_tooltip = None
            
            # 清理临时文件
            try:
                # 保留备份，但清理解压的文件
                if os.path.exists(extract_dir):
                    logger.debug(f"清理临时解压目录: {extract_dir}")
                    shutil.rmtree(extract_dir, ignore_errors=True)
            except Exception as e:
                logger.warning(f"清理临时文件失败: {str(e)}")
            
            # 发出安装完成信号
            self.install_complete.emit()
            
            # 显示重启提示对话框
            QApplication.processEvents()
            restart_dialog = MessageBox(
                "更新完成",
                "更新已安装完成，需要重启应用以应用更新。\n是否立即重启？",
                QApplication.activeWindow()
            )
            
            if restart_dialog.exec():
                # 用户选择立即重启
                logger.info("用户选择立即重启应用")
                time.sleep(1)
                from settings import restart
                restart()
            else:
                logger.info("用户选择稍后重启应用")
            
        except Exception as e:
            logger.error(f"安装更新失败: {str(e)}")
            self.install_error.emit(f"安装更新失败: {str(e)}")
            if self.state_tooltip:
                self.state_tooltip.setState(False)
                self.state_tooltip = None

    def _update_files(self, source_dir, target_dir):
        """更新文件
        
        Args:
            source_dir: 源目录（解压的更新包）
            target_dir: 目标目录（应用目录）
        """
        # 要排除的文件和目录
        exclude_patterns = [
            r'\.git.*',
            r'log/.*',
            r'config\.ini',
            r'students\.json',
            r'.*\.pyc',
            r'__pycache__/.*'
        ]
        
        # 创建备份目录
        backup_dir = os.path.join(tempfile.gettempdir(), f"randpicker_backup_{int(time.time())}")
        os.makedirs(backup_dir, exist_ok=True)
        logger.info(f"创建备份目录: {backup_dir}")
        
        # 记录更新的文件数量
        updated_files = 0
        total_files = 0
        
        # 统计需要更新的文件总数
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                rel_path = os.path.relpath(root, source_dir)
                if rel_path == '.':
                    rel_path = ''
                rel_file_path = os.path.join(rel_path, file).replace('\\', '/')
                
                # 检查是否在排除列表中
                exclude = False
                for pattern in exclude_patterns:
                    if re.match(pattern, rel_file_path):
                        exclude = True
                        break
                
                if not exclude:
                    total_files += 1
        
        # 更新状态提示
        if self.state_tooltip:
            self.state_tooltip.setContent(f"正在更新文件 (0/{total_files})")
        
        # 遍历源目录
        for root, dirs, files in os.walk(source_dir):
            # 计算相对路径
            rel_path = os.path.relpath(root, source_dir)
            if rel_path == '.':
                rel_path = ''
            
            # 创建目标目录
            target_path = os.path.join(target_dir, rel_path)
            os.makedirs(target_path, exist_ok=True)
            
            # 复制文件
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_path, file)
                rel_file_path = os.path.join(rel_path, file).replace('\\', '/')
                
                # 检查是否在排除列表中
                exclude = False
                for pattern in exclude_patterns:
                    if re.match(pattern, rel_file_path):
                        exclude = True
                        break
                
                if not exclude:
                    # 如果目标文件存在，先备份
                    if os.path.exists(dst_file):
                        backup_path = os.path.join(backup_dir, rel_path)
                        os.makedirs(backup_path, exist_ok=True)
                        backup_file = os.path.join(backup_path, file)
                        try:
                            shutil.copy2(dst_file, backup_file)
                        except Exception as e:
                            logger.warning(f"备份文件失败 {rel_file_path}: {str(e)}")
                    
                    # 复制新文件
                    try:
                        shutil.copy2(src_file, dst_file)
                        updated_files += 1
                        logger.debug(f"更新文件: {rel_file_path}")
                        
                        # 更新状态提示
                        if self.state_tooltip and total_files > 0:
                            progress = int(updated_files * 100 / total_files)
                            self.state_tooltip.setContent(f"正在更新文件 ({updated_files}/{total_files}) {progress}%")
                    except Exception as e:
                        logger.error(f"更新文件失败 {rel_file_path}: {str(e)}")
        
        logger.info(f"更新完成，共更新 {updated_files} 个文件")
        return updated_files

    def _compare_versions(self, version1, version2):
        """比较版本号
        
        Args:
            version1: 版本号1
            version2: 版本号2
            
        Returns:
            1 如果 version1 > version2
            0 如果 version1 == version2
            -1 如果 version1 < version2
        """
        v1_parts = list(map(int, version1.split('.')))
        v2_parts = list(map(int, version2.split('.')))
        
        # 补齐版本号部分
        while len(v1_parts) < 3:
            v1_parts.append(0)
        while len(v2_parts) < 3:
            v2_parts.append(0)
        
        # 比较版本号
        for i in range(3):
            if v1_parts[i] > v2_parts[i]:
                return 1
            elif v1_parts[i] < v2_parts[i]:
                return -1
        
        return 0


def check_for_updates(parent=None, silent=False):
    """检查更新的便捷函数
    
    Args:
        parent: 父窗口
        silent: 是否静默检查，不显示无更新提示
    
    Returns:
        Updater 实例
    """
    updater = Updater(parent)
    
    # 连接信号
    updater.update_available.connect(lambda version, notes: _show_update_dialog(updater, version, notes))
    updater.update_not_available.connect(lambda: _show_no_update_dialog(parent))
    updater.check_error.connect(lambda error: _show_error_dialog(parent, "检查更新失败", error))
    updater.download_error.connect(lambda error: _show_error_dialog(parent, "下载更新失败", error))
    updater.install_error.connect(lambda error: _show_error_dialog(parent, "安装更新失败", error))
    updater.download_complete.connect(updater.install_update)
    
    # 检查更新
    updater.check_for_updates(silent)
    
    return updater


def _show_update_dialog(updater, version, notes):
    """显示更新对话框
    
    Args:
        updater: 更新管理器
        version: 新版本号
        notes: 更新说明
    """
    dialog = Dialog(
        "发现新版本",
        f"发现新版本 {version}\n\n更新说明:\n{notes}\n\n是否现在更新？",
        QApplication.activeWindow()
    )
    
    # 设置按钮
    download_btn = PrimaryPushButton("立即更新")
    view_btn = PushButton("查看发布页")
    cancel_btn = PushButton("稍后再说")
    
    # 清空原有按钮布局
    while dialog.buttonLayout.count():
        item = dialog.buttonLayout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
    
    # 添加按钮到对话框
    dialog.yesButton = download_btn
    dialog.cancelButton = cancel_btn
    
    # 将按钮添加到布局
    dialog.buttonLayout.addWidget(download_btn)
    dialog.buttonLayout.addWidget(view_btn)
    dialog.buttonLayout.addWidget(cancel_btn)
    
    # 设置按钮间距和对齐方式
    dialog.buttonLayout.setSpacing(10)
    dialog.buttonLayout.setContentsMargins(0, 10, 0, 0)
    
    # 绑定事件
    download_btn.clicked.connect(updater.download_update)
    download_btn.clicked.connect(dialog.close)  # 点击后关闭对话框
    view_btn.clicked.connect(lambda: QDesktopServices.openUrl(
        QUrl(f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/latest")
    ))
    cancel_btn.clicked.connect(dialog.close)
    
    # 显示对话框
    dialog.exec()


def _show_no_update_dialog(parent):
    """显示无更新对话框
    
    Args:
        parent: 父窗口
    """
    InfoBar.success(
        title="已是最新版本",
        content=f"当前版本 {CURRENT_VERSION} 已是最新版本",
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=3000,
        parent=QApplication.activeWindow() or parent
    )


def _show_error_dialog(parent, title, message):
    """显示错误对话框
    
    Args:
        parent: 父窗口
        title: 标题
        message: 错误信息
    """
    InfoBar.error(
        title=title,
        content=message,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=5000,
        parent=QApplication.activeWindow() or parent
    )