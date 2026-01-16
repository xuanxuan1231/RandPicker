"""
随机选择
"""
from typing import Any

from PySide6.QtCore import QObject, Signal, Slot
from loguru import logger
from random import choices

class ChoiceMaker(QObject):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.studentsConfig = self.parent.studentsConfig
        self.notificationManager = self.parent.notificationManager
        self._refresh()

    def _refresh(self):
        self.students = self.studentsConfig.get_enabled_students()
        self.students_weights = self.studentsConfig.get_partof_students_weights(self.students)

    @Slot(int, bool, result=list)
    def choosePeople(self, number: int = 1, notify: bool = True) -> list[Any] | None:
        """随机选择学生"""
        self._refresh()
        if len(self.students) == 0:
            logger.warning("没有可用的学生进行选择。")
            return None
        if number > len(self.students):
            number = len(self.students)
        result = choices(self.students, weights=self.students_weights, k=number)
        logger.info(f"选择结果: {result}")
        if notify:
            self.notificationManager.send(
                option="native",
                title=f"抽选了 {number} 名学生",
                message=", ".join([self.studentsConfig.get_single_student(s).get("name", "未知") for s in result])
            )
            return None
        else:
            final_result = []
            for student_id in result:
                student = self.studentsConfig.get_single_student(student_id).copy()
                student["properties"] = self.studentsConfig.getProperty(student_id)
                student["avatar"] = self.studentsConfig.getAvatarPath(student_id)
                final_result.append(student)
            return final_result

    def advancedChoose(self):
        """ TODO)) 高级抽选"""
        pass