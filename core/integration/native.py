"""
向系统发送通知
"""

from loguru import logger
from plyer import notification


class NativeNotifier:
    def __init__(self):
        pass

    def send_message(self, pick_type: str, stus: list) -> bool:
        """发送通知消息"""
        try:
            title, message = self._format_message(pick_type, stus)
            self._send(title, message)
            return True
        except Exception as e:
            logger.error(f"Native 通知发送失败: {e}")
            return False

    def send_test(self) -> None:
        """发送测试通知"""
        try:
            title = "测试通知"
            message = "这是一条来自 RandPicker 的测试通知。"
            self._send(title, message)
        except Exception as e:
            logger.error(f"Native 测试通知发送失败: {e}")

    @staticmethod
    def _format_message(pick_type: str, stus: list) -> tuple[str, str]:
        """格式化通知消息"""
        # TODO)) 预埋：从设置中读取标题和内容格式
        title = f"抽选了 {len(stus)} " + ("名学生" if pick_type == "person" else "个小组")
        message = ", ".join(stus)
        return title, message

    @staticmethod
    def _send(title: str, message: str) -> None:
        """发送系统通知"""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="RandPicker",
            )
            logger.success(f"Native 通知发送成功: {title}: {message}")
        except Exception as e:
            logger.error(f"Native 通知发送失败: {e}")


nativeNotifier = NativeNotifier()
