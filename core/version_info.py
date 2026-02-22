import os

from PySide6.QtCore import QObject, Slot
from loguru import logger
from packaging.version import Version

VERSION = Version("2.0.0")
CODENAME = "JellyCat"


class VersionInfo(QObject):
    def __init__(self):
        super().__init__()

        self._commit_hash = os.popen("git rev-parse --short HEAD").read().replace("\n", "") or "未知"
        self._branch_name = os.popen("git branch --show-current").read().replace("\n", "") or "未知"
        self._is_dev = self._commit_hash != "未知" and self._branch_name != "未知"
        if self._is_dev:
            logger.warning("你正在启动 RandPicker 的开发预览版本，部分功能可能不稳定。")
            logger.info(f"你正在 {self._branch_name} 分支的 {self._commit_hash} 提交上。下一版本: {str(VERSION)}")
        else:
            logger.info(f"RandPicker {str(VERSION)} (Codename: {CODENAME})")

    @Slot(result=str)
    def getCommitHash(self) -> str:
        """获取当前的 Git 提交哈希值"""
        return self._commit_hash

    @Slot(result=str)
    def getBranchName(self) -> str:
        """获取当前的 Git 分支名称"""
        return self._branch_name

    @Slot(result=bool)
    def getAvailability(self) -> bool:
        """检查 Git 信息是否可用"""
        return self._is_dev

    def getVersion(self) -> str:
        """获取当前版本"""
        return str(VERSION)

    def getCodename(self) -> str:
        """获取当前版本代号"""
        return CODENAME


versionInfo = VersionInfo()
