"""
管理学生数据
"""

import json
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from PySide6.QtCore import QObject, Slot
from loguru import logger

from .dirs import CONFIG_DIR

DEFAULT_CONFIG = {
    "students": [
        {
            "id": "",
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
        # 维护两份配置：写入缓冲区与读取快照
        self.config_write = None
        self.config_read = None
        self.file = Path(CONFIG_DIR) / "students.json"
        self.load_config(DEFAULT_CONFIG)

    def load_config(self, default_config):
        if self.file.exists():
            with open(self.file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
        else:
            logger.info("未找到学生配置文件。将写入默认配置。")
            if default_config is None:
                logger.warning('未找到默认配置。使用空配置代替。')
                default_config = {}
            loaded = default_config  # 如果文件不存在，使用默认配置
            # 持久化默认配置
            try:
                if not Path(CONFIG_DIR).exists():
                    Path(CONFIG_DIR).mkdir(parents=True)
                with open(self.file, "w", encoding="utf-8") as f:
                    json.dump(loaded, f, ensure_ascii=False, indent=4)
            except Exception as e:
                logger.error(f"保存 默认 学生配置时出现错误: {e}")
        # 初始化读写两份配置
        self.config_write = deepcopy(loaded)
        self.config_read = deepcopy(loaded)
        # 为所有学生补充 GUID
        self._ensure_student_ids(self.config_write)
        self._ensure_student_ids(self.config_read)
        # 如果有新增 id，持久化一次，避免后续缺失
        try:
            if not Path(CONFIG_DIR).exists():
                Path(CONFIG_DIR).mkdir(parents=True)
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.config_write, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"保存 学生 GUID 时出现错误: {e}")

    def _ensure_student_ids(self, cfg: dict) -> None:
        """确保学生都有唯一 GUID。就地修改。"""
        if cfg is None:
            return
        students = cfg.setdefault("students", [])
        for stu in students:
            if not isinstance(stu, dict):
                continue
            if not stu.get("id"):
                stu["id"] = str(uuid4())

    def _find_index_by_guid(self, guid: str, use_write: bool = False) -> int:
        """根据 GUID 查找学生索引，找不到返回 -1。use_write=True 时使用写缓冲。"""
        source = self.config_write if use_write else self.config_read
        s = (source or {}).get("students", []) if source else []
        for idx, stu in enumerate(s):
            if stu.get("id") == guid:
                return idx
        return -1

    @Slot()
    def save_config(self):
        try:
            # 确保配置文件目录存在
            if not Path(CONFIG_DIR).exists():
                Path(CONFIG_DIR).mkdir(parents=True)
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.config_write, f, ensure_ascii=False, indent=4)
            # 保存后刷新读取快照
            self.config_read = deepcopy(self.config_write)
            logger.success("学生配置已保存，并刷新读取快照。")
        except Exception as e:
            logger.error(f"保存 设置 配置时出现错误: {e}")

    @Slot(result=list)
    def get_students(self) -> list:
        """
        获取所有学生的列表。

        :return: 学生列表
        """
        # 读取使用快照
        cfg = self.config_read or {}
        s = cfg.get("students", [])
        if s is None:
            logger.warning("学生列表为空, 返回空列表。")
            return []
        return s

    @Slot(result=list)
    def get_enabled_students(self) -> list:
        """返回启用学生的 GUID 列表。"""
        s = self.get_students()
        ids = []
        for stu in s:
            if stu.get("enabled", False):
                ids.append(stu.get("id"))
        return ids

    @Slot(list, result=list)
    def get_partof_students_weights(self, guids: list) -> list:
        """根据 GUID 列表返回对应学生的权重。"""
        if not guids:
            return []
        weights = []
        for guid in guids:
            student = self.get_single_student(guid)
            weights.append(student.get("weight", 1))
        return weights

    @Slot(str, result=dict)
    def get_single_student(self, guid: str) -> dict:
        """根据 GUID 获取单个学生的信息。找不到返回空字典。"""
        if not guid:
            logger.error("学生 GUID 为空。")
            return {}
        idx = self._find_index_by_guid(guid)
        if idx == -1:
            logger.error(f"未找到 GUID 为 {guid} 的学生。")
            return {}
        s = self.get_students()
        return s[idx]

    @Slot(str, int, bool)
    def add_student(self, name: str, weight: int = 1, enabled: bool = True) -> None:
        new_student = {
            "name": name,
            "weight": weight,
            "enabled": enabled,
            "id": str(uuid4())
        }
        # 写入缓冲区
        if self.config_write is None:
            self.config_write = {"students": []}
        self.config_write.setdefault("students", []).append(new_student)
        logger.success(f"在缓冲区添加学生 {name}。")

    @Slot(str)
    def remove_student(self, guid: str) -> None:
        s = self.config_write.setdefault("students", [])
        idx = self._find_index_by_guid(guid, use_write=True)
        if idx == -1:
            logger.error(f"学生 GUID {guid} 未找到, 无法删除。")
            return
        name = s[idx].get("name", "未知")
        self.config_write["students"].pop(idx)
        logger.success(f"在缓冲区已删除学生 {name}。GUID: {guid}")

    @Slot(str, result=str)
    def getAvatarPath(self, guid: str):
        """
        获取学生头像路径。
        因为这个需要检验路径是否存在，所以要单开一个 function。

        """
        if not guid:
            logger.info("GUID 为空。返回空路径。")
            return ""
        student = self.get_single_student(guid)
        avatar_path = student.get("avatar", "")
        if avatar_path == "":
            return ""
        avatar_file = Path(avatar_path)
        if not avatar_file.exists():
            logger.warning(f"学生 GUID {guid} 的头像文件不存在: {avatar_path}")
            return ""
        return str(avatar_file.resolve())

    @Slot(str, result=list)
    def getProperty(self, guid: str) -> list:
        if not guid:
            logger.info("GUID 为空。返回示例。")
            return [{"name": "没有附加属性", "value": "没有附加属性值"}]
        student = self.get_single_student(guid)
        return student.get("properties", [{"name": "没有附加属性", "value": "没有附加属性值"}])

    @Slot(result=dict)
    def getBuffer(self):
        """
        返回写入缓冲区的副本，避免外部代码直接修改内部缓冲区。
        """
        if self.config_write is None:
            return None
        return deepcopy(self.config_write)
