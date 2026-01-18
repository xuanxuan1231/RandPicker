"""
向 ClassIsland 发送通知

"""

from PySide6.QtCore import QObject, Slot


class ClassIslandIntegration(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str, str, str)
    def send_notification(self, title: str, message: str, url: str):
        """
        发送通知到 ClassIsland

        :param title: 通知标题
        :param message: 通知内容
        :param url: 通知链接
        """
        # 这里添加实际的通知发送逻辑
        print(f"Sending notification to ClassIsland:\nTitle: {title}\nMessage: {message}\nURL: {url}")