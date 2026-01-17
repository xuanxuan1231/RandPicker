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
        students = self.studentsConfig.get_students()
        self.students = []
        self.students_weights = []
        for student in students:
            if student.get("enabled", False):
                self.students.append(student.get("guid"))
                self.students_weights.append(student.get("weight", 1))

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
            students_list = self.studentsConfig.get_students()
            names = []
            for guid in result:
                for student in students_list:
                    if student.get("guid") == guid:
                        names.append(student.get("name", "未知"))
                        break
            self.notificationManager.send(
                option="native",
                title=f"抽选了 {number} 名学生",
                message=", ".join(names)
            )
            return None
        else:
            final_result = []
            students_list = self.studentsConfig.get_students()
            for guid in result:
                for student in students_list:
                    if student.get("guid") == guid:
                        student_copy = student.copy()
                        student_copy["properties"] = student.get("properties", [])
                        student_copy["avatar"] = student.get("avatar", "")
                        final_result.append(student_copy)
                        break
            return final_result

    def advancedChoose(self):
        """ TODO)) 高级抽选"""
        pass