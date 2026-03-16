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
from ..integration import NotificationManager
from .excel_import import ExcelImporter

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
    _instance: "StudentsConfig" = None

    @classmethod
    def instance(cls) -> "StudentsConfig":
        return cls._instance

    def __init__(self, parent=None):
        super().__init__()
        StudentsConfig._instance = self
        # 维护两份配置：写入缓冲区与读取快照
        self.config_write = None
        self.config_read = None
        self.file = Path(CONFIG_DIR) / "students.json"
        self.load_config(DEFAULT_CONFIG)

    def load_config(self, default_config):
        if self.file.exists():
            try:
                with open(self.file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                if not isinstance(loaded, dict):
                    logger.error("学生配置文件格式不正确（非字典），将使用默认配置。")
                    loaded = deepcopy(default_config) if default_config else {}
            except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
                logger.error(f"读取学生配置文件失败，将使用默认配置: {e}")
                loaded = deepcopy(default_config) if default_config else {}
                nm = NotificationManager.instance()
                if nm is not None:
                    nm.send_raw(
                        "RandPicker - 配置文件损坏",
                        f"学生配置文件无法读取，已使用默认配置。\n错误: {e}",
                        "native"
                    )
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
                logger.exception(f"保存 默认 学生配置时出现错误: {e}")
        # 初始化读写两份配置
        self.config_write = deepcopy(loaded)
        # 先为写缓冲补充 GUID，再从写缓冲复制到读快照，
        # 确保两份配置中的学生 GUID 一致。
        self._ensure_student_ids(self.config_write)
        self.config_read = deepcopy(self.config_write)
        # 如果有新增 id，持久化一次，避免后续缺失
        try:
            if not Path(CONFIG_DIR).exists():
                Path(CONFIG_DIR).mkdir(parents=True)
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.config_write, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.exception(f"保存 学生 GUID 时出现错误: {e}")

    def _ensure_student_ids(self, cfg: dict) -> None:
        """确保学生都有唯一 GUID，并补全缺失字段。就地修改。"""
        if cfg is None:
            return
        # 确保 students 是列表
        students = cfg.get("students")
        if not isinstance(students, list):
            cfg["students"] = []
            students = cfg["students"]
        # 过滤掉非字典的无效条目
        cfg["students"] = [stu for stu in students if isinstance(stu, dict)]
        students = cfg["students"]
        for stu in students:
            if not stu.get("id"):
                stu["id"] = str(uuid4())
            # 补全可能缺失的字段（兼容旧版配置）
            stu.setdefault("name", "未命名")
            stu.setdefault("weight", 1.0)
            stu.setdefault("enabled", True)
            stu.setdefault("avatar", "")
            stu.setdefault("properties", [])

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
            logger.exception(f"保存 设置 配置时出现错误: {e}")

    @Slot()
    def reload_config(self):
        """从磁盘重新加载配置，丢弃写缓冲区的所有未保存更改。"""
        self.load_config(DEFAULT_CONFIG)
        logger.success("已从磁盘重新加载学生配置，写缓冲区已重置。")

    @Slot(result=bool)
    def has_unsaved_changes(self) -> bool:
        """比较写缓冲区与读取快照，判断是否有未保存的更改。"""
        return self.config_write != self.config_read

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

    @Slot(str, float, bool)
    def add_student(self, name: str, weight: float = 1.0, enabled: bool = True) -> None:
        # 验证并清理输入
        name = (name or "").strip()
        if not name:
            name = "未命名"
        weight = max(0.0, float(weight))
        new_student = {
            "name": name,
            "weight": weight,
            "enabled": enabled,
            "id": str(uuid4()),
            "avatar": "",
            "properties": []
        }
        # 写入缓冲区
        if self.config_write is None:
            self.config_write = {"students": []}
        self.config_write.setdefault("students", []).append(new_student)
        logger.success(f"在缓冲区添加学生 {name}。")

    @Slot(str)
    def remove_student(self, guid: str) -> None:
        if self.config_write is None:
            logger.error("写缓冲区为空，无法删除学生。")
            return
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
        try:
            avatar_file = Path(avatar_path)
            if not avatar_file.exists():
                logger.warning(f"学生 GUID {guid} 的头像文件不存在: {avatar_path}")
                return ""
            return str(avatar_file.resolve())
        except (OSError, ValueError) as e:
            logger.warning(f"学生 GUID {guid} 的头像路径无效或无权访问: {avatar_path}, 错误: {e}")
            return ""

    @Slot(str, result=list)
    def getProperty(self, guid: str) -> list:
        if not guid:
            logger.info("GUID 为空。返回示例。")
            return [{"name": "没有附加属性", "value": "没有附加属性值"}]
        student = self.get_single_student(guid)
        return student.get("properties", [{"name": "没有附加属性", "value": "没有附加属性值"}])

    @Slot(str, str, float, bool, str)
    def update_student(self, guid: str, name: str, weight: float, enabled: bool, avatar: str) -> None:
        """根据 GUID 更新学生基础信息（写缓冲区）。"""
        idx = self._find_index_by_guid(guid, use_write=True)
        if idx == -1:
            logger.error(f"更新失败：未找到 GUID {guid}")
            return
        # 验证并清理名称
        name = (name or "").strip()
        if not name:
            logger.warning(f"学生名称为空，将使用默认名称。GUID: {guid}")
            name = "未命名"
        # 验证权重
        weight = max(0.0, float(weight))
        # 验证头像路径安全性
        safe_avatar = ""
        if avatar:
            try:
                # 允许绝对路径（跨平台：Unix / 开头，Windows 盘符如 C:/ 开头）
                is_abs = avatar.startswith("/") or (len(avatar) >= 3 and avatar[1] == ":" and avatar[2] in ("/", "\\"))
                if is_abs:
                    safe_avatar = avatar
                else:
                    logger.warning(f"头像路径不是绝对路径，已忽略: {avatar}")
            except (OSError, ValueError) as e:
                logger.warning(f"头像路径无效，已忽略: {avatar}, 错误: {e}")
        stu = self.config_write["students"][idx]
        stu["name"] = name
        stu["weight"] = weight
        stu["enabled"] = enabled
        stu["avatar"] = safe_avatar
        logger.success(f"缓冲区已更新学生 {name}（GUID: {guid}）")

    @Slot(str, list)
    def update_student_properties(self, guid: str, properties: list) -> None:
        """根据 GUID 替换学生附加属性列表（写缓冲区）。"""
        idx = self._find_index_by_guid(guid, use_write=True)
        if idx == -1:
            logger.error(f"更新附加属性失败：未找到 GUID {guid}")
            return
        # 验证并清理属性列表
        cleaned = []
        for prop in (properties or []):
            if not isinstance(prop, dict):
                continue
            cleaned.append({
                "name": str(prop.get("name", "")).strip(),
                "value": str(prop.get("value", "")).strip()
            })
        self.config_write["students"][idx]["properties"] = cleaned
        logger.success(f"缓冲区已更新学生附加属性（GUID: {guid}）")

    @Slot(result=list)
    def get_write_students(self) -> list:
        """返回写缓冲中的学生列表（副本），供 QML 编辑页面使用。"""
        cfg = self.config_write or {}
        students = cfg.get("students", [])
        return deepcopy(students)

    @Slot(str, result=dict)
    def get_write_student(self, guid: str) -> dict:
        """根据 GUID 从写缓冲中获取单个学生信息。"""
        if not guid:
            return {}
        idx = self._find_index_by_guid(guid, use_write=True)
        if idx == -1:
            return {}
        return deepcopy(self.config_write["students"][idx])

    @Slot(result=dict)
    def getBuffer(self):
        """
        返回写入缓冲区的副本，避免外部代码直接修改内部缓冲区。
        """
        if self.config_write is None:
            return None
        return deepcopy(self.config_write)

    @Slot(str, str, result=str)
    def import_students_from_excel(self, file_path: str, import_mode: str = "replace") -> str:
        """
        从 Excel 文件导入学生列表。

        :param file_path: Excel 文件路径
        :param import_mode: 导入模式 "replace" (替换全部) 或 "merge" (合并追加)
        :return: 结果消息
        """
        students, message = ExcelImporter.import_from_excel(file_path, import_mode)

        if not students:
            logger.error(f"导入失败: {message}")
            return f"导入失败: {message}"

        # 根据导入模式处理
        if import_mode == "replace":
            # 替换模式：清空现有学生列表
            self.config_write["students"] = students
            logger.info(f"已替换全部学生数据，共 {len(students)} 名学生")
        elif import_mode == "merge":
            # 合并模式：追加到现有列表
            existing = self.config_write.get("students", [])
            existing.extend(students)
            self.config_write["students"] = existing
            logger.info(f"已合并学生数据，新增 {len(students)} 名学生")
        else:
            return f"未知的导入模式: {import_mode}"

        return message

    @Slot(str, result=str)
    def export_students_to_excel(self, file_path: str) -> str:
        """
        导出学生列表到 Excel 文件。

        :param file_path: 输出文件路径
        :return: 结果消息
        """
        students = self.get_write_students()
        success, message = ExcelImporter.export_to_excel(file_path, students)

        if success:
            logger.success(message)
        else:
            logger.error(message)

        return message

    @Slot(result=bool)
    def is_excel_available(self) -> bool:
        """检查 Excel 导入导出功能是否可用"""
        return ExcelImporter.is_available()
