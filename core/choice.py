"""
随机选择
"""

from PySide6.QtCore import QObject, Signal, Slot
from loguru import logger
from random import choices

class ChoiceMaker(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.studentsConfig = self.parent.studentsConfig
        self.notificationManager = self.parent.notificationManager
        self._refresh()

    def _refresh(self):
        self.students = self.studentsConfig.get_enabled_students()
        self.students_weights = self.studentsConfig.get_partof_students_weights(self.students)

    @Slot(int)
    def choosePeople(self, number: int = 1):
        """随机选择学生"""
        self._refresh()
        if len(self.students) == 0:
            logger.warning("没有可用的学生进行选择。")
            return
        if number > len(self.students):
            number = len(self.students)
        result = choices(self.students, weights=self.students_weights, k=number)
        self.notificationManager.send(
            option="native",
            title=f"抽选了 {number} 名学生",
            message=", ".join([self.studentsConfig.get_single_student(s).get("name", "未知") for s in result])
        )
        logger.info(f"选择结果: {result}")