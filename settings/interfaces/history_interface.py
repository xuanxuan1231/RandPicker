"""RandPicker 历史记录界面。

此模块提供历史记录界面功能的实现。
"""
import json
import os
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from loguru import logger
from qfluentwidgets import (Flyout, InfoBarIcon, FlyoutAnimationType, PrimaryPushButton, 
                           ScrollArea, ExpandLayout, CardWidget, isDarkTheme)

import conf

HISTORY_FILE = './history.json'

def load_history():
    """加载抽奖历史记录。"""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        try:
            history = json.load(f)
            return history
        except json.JSONDecodeError:
            logger.error(f'历史记录文件 {HISTORY_FILE} 格式错误。')
            return []

def save_history(history):
    """保存抽奖历史记录。"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def add_history_entry(entry):
    """添加新的历史记录条目。"""
    history = load_history()
    history.append(entry)
    save_history(history)
    logger.info(f'已添加历史记录条目：{entry}')

def setup_history_interface(window):
    """设置历史记录页面。

    :param window: 设置窗口实例
    """
    # 获取原始UI中的控件容器
    history_container = window.historyInterface
    layout = history_container.findChild(QVBoxLayout, 'verticalLayout')
    
    # 移除旧的表格控件
    old_table = history_container.findChild(QWidget, 'historyTable')
    if old_table:
        layout.removeWidget(old_table)
        old_table.deleteLater()
    
    # 创建滚动区域和卡片布局
    scroll_area = ScrollArea(history_container)
    scroll_area.setObjectName('historyScrollArea')
    scroll_area.setWidgetResizable(True)
    
    # 创建内容容器和布局
    content_widget = QWidget(scroll_area)
    history_layout = ExpandLayout(content_widget)
    history_layout.setSpacing(10)
    history_layout.setContentsMargins(10, 10, 10, 10)
    content_widget.setLayout(history_layout)
    
    # 设置滚动区域的内容
    scroll_area.setWidget(content_widget)
    
    # 将滚动区域添加到布局中
    layout.insertWidget(1, scroll_area)
    
    clear_button = window.findChild(PrimaryPushButton, 'clearHistoryButton')

    # 加载并显示历史记录
    display_history(scroll_area)

    # 绑定清空按钮事件
    clear_button.clicked.connect(lambda: clear_history(window, scroll_area))

class HistoryCard(CardWidget):
    """历史记录卡片组件"""
    
    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.setup_ui()
        
    def setup_ui(self):
        # 设置卡片样式
        self.setFixedHeight(80)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(0)
        
        # 创建标题（时间和类型）
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        
        # 时间标签
        time_label = QLabel(self.entry['time'], self)
        time_label.setObjectName('TimeLabel')
        time_label.setStyleSheet('font-size: 14px; font-weight: 500;')
        
        # 类型标签
        type_text = '随机选人' if self.entry['type'] == 'person' else '随机选组'
        type_label = QLabel(type_text, self)
        type_label.setObjectName('TypeLabel')
        type_label.setStyleSheet('font-size: 12px; opacity: 0.6;')
        
        title_layout.addWidget(time_label)
        title_layout.addWidget(type_label)
        
        # 结果标签
        result_label = QLabel(self.entry['result'], self)
        result_label.setObjectName('ResultLabel')
        result_label.setStyleSheet('font-size: 15px; font-weight: 600; margin-top: 5px;')
        
        # 添加到主布局
        layout.addLayout(title_layout)
        layout.addWidget(result_label)

def display_history(scroll_area):
    """在滚动区域中显示历史记录。"""
    # 获取内容容器和布局
    content_widget = scroll_area.widget()
    layout = content_widget.layout()
    
    # 清空布局
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
    
    # 加载历史记录
    history = load_history()
    
    # 倒序显示历史记录（最新的在最上面）
    for entry in reversed(history):
        # 创建历史记录卡片
        card = HistoryCard(entry, content_widget)
        layout.addWidget(card)

def clear_history(window, scroll_area):
    """清空历史记录。"""
    save_history([])
    
    # 清空布局
    content_widget = scroll_area.widget()
    layout = content_widget.layout()
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
            
    logger.info('历史记录已清空。')

    # 显示清空成功提示
    Flyout.create(
        icon=InfoBarIcon.SUCCESS,
        title='历史记录已清空',
        content="抽奖历史记录已全部清除。",
        target=window.findChild(PrimaryPushButton, 'clearHistoryButton'),
        parent=window,
        isClosable=False,
        aniType=FlyoutAnimationType.PULL_UP
    )

# 在 main.py 中调用此函数来记录抽奖结果
# from settings.interfaces.history_interface import add_history_entry
# add_history_entry({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'type': 'person', 'result': f'{self.student['id']} {self.student['name']}'})
# add_history_entry({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'type': 'group', 'result': f'{group['name']} ({students})'})