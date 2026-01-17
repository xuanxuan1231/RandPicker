"""
管理学生数据
"""

from PySide6.QtCore import QObject, Slot
from loguru import logger
from .dirs import CONFIG_DIR
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "students": [
        {
            "name": "张三",
            "weight": 1,
            "enabled": True,
            "avatar": "",
            "properties": []
        }
    ]
}


class StudentsConfig(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.config = None
        self.file = Path(CONFIG_DIR) / "students.json"
        self.load_config(DEFAULT_CONFIG)

    def load_config(self, default_config):
        if self.file.exists():
            with open(self.file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            logger.info("未找到学生配置文件。将写入默认配置。")
            if default_config is None:
                logger.warning('未找到默认配置。使用空配置代替。')
                default_config = {}
            self.config = default_config  # 如果文件不存在，使用默认配置
            self.save_config()

    @Slot()
    def save_config(self):
        try:
            # 确保配置文件目录存在
            if not Path(CONFIG_DIR).exists():
                Path(CONFIG_DIR).mkdir(parents=True)
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"保存 设置 配置时出现错误: {e}")

    @Slot(result=list)
    def get_students(self) -> list:
        """
        获取所有学生的列表。

        :return: 学生列表
        """
        s = self.config.get("students", [])
        if s is None:
            logger.warning("学生列表为空, 返回空列表。")
        return s

    def get_enabled_students(self) -> list:
        """
        获取所有启用状态的学生 ID 列表。
        这个只应被 Python 调用，因此只返回 ID 列表。

        :return: 启用状态的学生 ID
        """
        s = self.get_students()
        enabled_students = []
        for index, student in enumerate(s):
            if student.get("enabled", False):
                enabled_students.append(index)
        return enabled_students

    def get_filtered_students(self, filters: list[dict] = None) -> list:
        """
        获取符合筛选条件的启用状态学生 ID 列表。

        :param filters: 筛选条件列表，例如 [{"name": "bar", "value": "foo"}]
        :return: 符合条件的启用状态学生 ID 列表
        """
        enabled_ids = self.get_enabled_students()
        if not filters:
            return enabled_ids

        filtered_ids = []
        for stu_id in enabled_ids:
            student = self.get_single_student(stu_id)
            properties = student.get("properties", [])
            
            # 检查是否满足所有筛选条件
            match_all = True
            for f in filters:
                f_name = f.get("name")
                f_value = f.get("value")
                
                # 在学生的 properties 中查找匹配项
                found = False
                for p in properties:
                    if p.get("name") == f_name and p.get("value") == f_value:
                        found = True
                        break
                
                if not found:
                    match_all = False
                    break
            
            if match_all:
                filtered_ids.append(stu_id)
        
        return filtered_ids

    def get_partof_students_weights(self, stuIds: list) -> list:
        """
        获取部分学生的权重列表。
        这个只应被 Python 调用，因此只返回权重列表。

        :param stuIds: 学生 ID 列表
        :return: 请求的学生权重
        """
        weights = []
        for student in stuIds:
            s = self.get_single_student(student)
            weights.append(s.get("weight", 1))
        return weights

    @Slot(int, result=dict)
    def get_single_student(self, stuId: int) -> dict:
        """
        获取单个学生的信息。

        :param stuId: 学生 ID
        :return: 学生信息
        """
        s = self.get_students()
        if stuId < 0 or stuId >= len(s):
            logger.error(f"学生 ID {stuId} 超出范围。")
            return {}
        return s[stuId]

    @Slot(str, int, bool)
    def add_student(self, name: str, weight: int = 1, enabled: bool = True) -> None:
        new_student = {
            "name": name,
            "weight": weight,
            "enabled": enabled
        }
        self.config["students"].append(new_student)
        logger.success(f"在缓冲区添加学生 {name}。")

    @Slot(int)
    def remove_student(self, stuId: int) -> None:
        s = self.get_students()
        name = self.get_single_student(stuId)["name"]
        if stuId < 0 or stuId >= len(s):
            logger.error(f"学生 ID {stuId} 超出范围, 无法删除。")
            return
        self.config["students"].pop(stuId)
        logger.success(f"在缓冲区已删除学生 {name}。ID: {stuId}")

    @Slot(int)
    def getAvatarPath(self, stuId: int):
        """
        获取学生头像路径。
        因为这个需要检验路径是否存在，所以要单开一个 function。

        """
        if not isinstance(stuId, int):
            logger.error(f"学生 ID 类型错误: {type(stuId)}，应为 int。")
            return ""
        if stuId == -1:
            logger.info("ID 是保留的 -1。返回空路径。")
            return ""
        student = self.get_single_student(stuId)
        avatar_path = student.get("avatar", "")
        if avatar_path == "":
            return ""
        avatar_file = Path(avatar_path)
        if not avatar_file.exists():
            logger.warning(f"学生 ID {stuId} 的头像文件不存在: {avatar_path}")
            return ""
        return str(avatar_file.resolve())

    @Slot(int, result=list)
    def getProperty(self, stuId: int) -> list:
        if stuId == -1:
            logger.info("ID 是保留的 -1。返回示例。")
            return [{"name": "没有附加属性", "value": "没有附加属性值"}]
        student = self.get_single_student(stuId)
        return student.get("properties", [{"name": "没有附加属性", "value": "没有附加属性值"}])
