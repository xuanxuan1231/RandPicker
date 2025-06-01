"""RandPicker 崩溃处理模块

此模块提供崩溃日志处理和自动显示功能。
"""
import os
import glob
import sys
import traceback
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QTextEdit, QDialog
from PyQt6.QtCore import Qt
from loguru import logger
from qfluentwidgets import Dialog, PrimaryPushButton, TitleLabel, BodyLabel, InfoBar, InfoBarPosition


def get_latest_log_file():
    """获取最新的日志文件"""
    # 确保日志目录存在
    os.makedirs("./log", exist_ok=True)
    log_files = glob.glob('./log/RandPicker_*.log')
    if not log_files:
        return None
    return max(log_files, key=os.path.getmtime)


def parse_log_for_human(log_path):
    """将日志内容翻译为普通人可读的摘要"""
    if not log_path or not os.path.exists(log_path):
        return "未找到日志文件。"
    
    lines = []
    with open(log_path, 'r', encoding='utf-8') as f:
        for l in f:
            if any(x in l for x in ["ERROR", "EXCEPTION", "CRITICAL", "Traceback"]):
                lines.append(l.strip())
    
    if not lines:
        return "未检测到异常信息，程序可能正常退出。"
    
    # 简单翻译
    result = ["检测到程序异常退出，以下为主要错误信息："]
    for l in lines:
        if "Traceback" in l:
            result.append("发生了程序崩溃（Traceback），请联系开发者。"); continue
        if "ERROR" in l or "CRITICAL" in l:
            # 只保留关键信息
            msg = l.split("-", 1)[-1].strip() if "-" in l else l
            result.append("错误：" + msg)
        elif "EXCEPTION" in l:
            result.append("异常：" + l)
    
    return "\n".join(result)


class LogViewerDialog(Dialog):
    """日志查看器对话框"""
    def __init__(self, log_content, parent=None):
        super().__init__("程序异常日志", "", parent)
        self.resize(600, 400)
        
        # 创建日志内容显示区域
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.log_text.setPlainText(log_content)
        self.log_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        # 添加到布局
        self.viewLayout.addWidget(TitleLabel("程序异常日志"))
        self.viewLayout.addWidget(BodyLabel("检测到上次程序异常退出，以下是错误日志的人性化解释："))
        self.viewLayout.addWidget(self.log_text)
        
        # 设置按钮
        self.yesButton.setText("我知道了")
        self.cancelButton.hide()


def check_crash_on_startup():
    """在启动时检查是否存在崩溃日志，如果有则显示"""
    latest_log = get_latest_log_file()
    if not latest_log:
        return
    
    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            content = f.read()
            if any(x in content for x in ["ERROR", "EXCEPTION", "CRITICAL", "Traceback"]):
                # 解析日志内容
                human_readable_log = parse_log_for_human(latest_log)
                
                # 创建并显示日志查看器对话框
                app = QApplication.instance()
                if app:
                    dialog = LogViewerDialog(human_readable_log)
                    dialog.exec()
    except Exception as e:
        logger.error(f"检查崩溃日志时出错: {e}")


def setup_exception_handler():
    """设置全局异常处理器"""
    def exception_handler(exctype, value, tb):
        # 记录异常到日志
        error_msg = ''.join(traceback.format_exception(exctype, value, tb))
        logger.error(f"未捕获的异常: {error_msg}")
        
        # 尝试显示错误对话框
        try:
            app = QApplication.instance()
            if app:
                dialog = Dialog(
                    "程序发生错误", 
                    f"程序遇到了一个问题需要关闭。\n\n错误信息: {str(value)}\n\n详细日志已保存，下次启动时将自动显示。"
                )
                dialog.yesButton.setText("关闭程序")
                dialog.cancelButton.hide()
                dialog.exec()
        except:
            pass
        
        # 调用原始的异常处理器
        sys.__excepthook__(exctype, value, tb)
    
    # 设置全局异常处理器
    sys.excepthook = exception_handler


# 在导入模块时自动设置异常处理器
setup_exception_handler()