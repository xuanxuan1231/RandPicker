"""
随机选择
"""
from random import choices
from typing import Any

from PySide6.QtCore import QObject, Slot, Signal, Property
from loguru import logger

from .config.students import StudentsConfig
from .integration import NotificationManager


class ChoiceMaker(QObject):
    _instance: "ChoiceMaker" = None

    # 记忆模式和变化信号
    memoryEnabledChanged = Signal(bool)

    @classmethod
    def instance(cls) -> "ChoiceMaker":
        return cls._instance

    def __init__(self, parent=None):
        super().__init__()
        ChoiceMaker._instance = self
        self.studentsConfig = StudentsConfig.instance()
        self.notificationManager = NotificationManager.instance()
        self._refresh()

        # 记忆模式状态
        self._memory_enabled = False
        # 一选
        self._memory_set: set = set()

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

        # 记忆模式前处理
        available_students = list(self.students)
        available_weights = list(self.students_weights)
        if self._memory_enabled:
            pairs = [(s, w) for s, w in zip(available_students, available_weights) if s not in self._memory_set]
            if not pairs:
                # 自动清空会话内记忆，允许重新从全部学生中抽选
                self._memory_set.clear()
            else:
                available_students, available_weights = map(list, zip(*pairs))

        if number > len(available_students):
            number = len(available_students)

        # 不重复抽样
        result = []
        temp_students = list(available_students)
        temp_weights = list(available_weights)
        for _ in range(number):
            pick = choices(temp_students, weights=temp_weights, k=1)[0]
            result.append(pick)
            idx = temp_students.index(pick)
            temp_students.pop(idx)
            temp_weights.pop(idx)
        logger.info(f"选择结果: {result}")

        # 发送通知
        if notify:
            self.notificationManager.send(
                # title=f"抽选了 {number} 名学生",
                pick_type="person",
                # message=", ".join([self.studentsConfig.get_single_student(s).get("name", "未知") for s in result])
                stus=[self.studentsConfig.get_single_student(s) for s in result]
            )
            # 记忆模式下记录已抽中的学生
            if self._memory_enabled:
                for student_id in result:
                    self._memory_set.add(student_id)
            return None
        else:
            final_result = []
            for student_id in result:
                student = self.studentsConfig.get_single_student(student_id).copy()
                student["properties"] = self.studentsConfig.getProperty(student_id)
                student["avatar"] = self.studentsConfig.getAvatarPath(student_id)
                final_result.append(student)
            if self._memory_enabled:
                for student_id in result:
                    self._memory_set.add(student_id)
            return final_result

    def advancedChoose(self):
        """ TODO)) 高级抽选"""
        pass

    @Property(bool, notify=memoryEnabledChanged)
    def memoryEnabled(self) -> bool:
        """获取当前会话内记忆模式状态"""
        return getattr(self, "_memory_enabled", False)

    @memoryEnabled.setter
    def memoryEnabled(self, enabled: bool) -> None:
        """启用/禁用会话内记忆模式（排除已选学生）"""
        self._memory_enabled = bool(enabled)
        try:
            self.memoryEnabledChanged.emit(self._memory_enabled)
        except Exception:
            pass

    @Slot()
    def resetMemory(self) -> None:
        """清除会话内记忆（重置已记录的已选学生）"""
        self._memory_set.clear()
