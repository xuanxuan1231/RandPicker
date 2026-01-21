"""
向 ClassIsland 发送通知

"""
import os
import sys

from PySide6.QtCore import QObject, Slot
from loguru import logger
from ..config.dirs import DLL_DIR


class ClassIslandIntegration(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_available = None
        self.initialize()

    def initialize(self):
        try:
            #import clr
            from pythonnet import load
            load("coreclr")
            import clr

            sys.path.append("./lib")
            clr.AddReference("ClassIsland.Shared.IPC")

            from ClassIsland.Shared.IPC import IpcClient
            from System.Threading.Tasks import Task

            self.IpcClient = IpcClient
            self.client = None
            self.routed_path = "RandPicker.Notify"
            self.is_available = True
            logger.info("成功加载 ClassIsland IPC 库")
            
        except Exception as e:
            logger.error(f"加载 ClassIsland 集成时发生错误: {e}")
            logger.warning("ClassIsland 集成在您的系统上可能不可用。")
            self.is_available = False

        self._connect_ipc()

    def _connect_ipc(self):
        try:
            if self.client is None:
                self.client = self.IpcClient()

            task = self.client.Connect()
            task.Wait()  # 同步等待连接任务完成

            if self.client.IsConnected:
                self.is_connected = True
                logger.success("IPC 连接已建立。")
            else:
                self.is_connected = False
                logger.warning("IPC 连接建立失败")
        except Exception as e:
            self.is_connected = False
            logger.error(f"建立 IPC 连接时出错: {e}")

    @Slot(result=str)
    def getStatus(self):
        try:
            if self.is_available:
                return "Connected" if self.is_connected else "NotConnected"
            else:
                return "NotAvailable"
        except Exception as e:
            logger.warning("获取 ClassIsland 集成连接状态时出错。")
            return "Unknown"

    def send_notification(self, title: str, message: str, url: str):
        """
        发送通知到 ClassIsland

        :param title: 通知标题
        :param message: 通知内容
        :param url: 通知链接
        """
        # 这里添加实际的通知发送逻辑
        print(f"Sending notification to ClassIsland:\nTitle: {title}\nMessage: {message}\nURL: {url}")

    def get_availability(self):
        return self.is_available



ciService = ClassIslandIntegration()