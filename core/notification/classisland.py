"""
向 ClassIsland 发送通知 (通过 IPC)
"""
import socket
import json
from loguru import logger

class ClassIslandNotifier:
    def __init__(self):
        # 使用本地回环地址和约定的端口
        self.host = '127.0.0.1'
        self.port = 58210  # 约定的 IPC 端口

    def send(self, title: str, message: str) -> None:
        """通过 IPC 向 RandPicker_CI 发送通知请求"""
        data = {
            "title": title,
            "message": message
        }
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)  # 设置超时
                s.connect((self.host, self.port))
                s.sendall(json.dumps(data).encode('utf-8'))
                logger.info(f"已通过 IPC 发送通知到 ClassIsland: {title}")
        except Exception as e:
            logger.error(f"发送 IPC 通知失败: {e}")
