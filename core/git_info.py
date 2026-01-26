import os

from PySide6.QtCore import QObject, Slot
from loguru import logger

class GitInfo(QObject):
    def __init__(self):
        super().__init__()
        self._available = os.system("git branch --show-current") == 0
        self._commit_hash = os.popen("git rev-parse --short HEAD").read().replace("\n", "") or "未知"
        self._branch_name = os.popen("git branch --show-current").read().replace("\n", "") or "未知"
        logger.warning("你正在启动 RandPicker 的开发预览版本，部分功能可能不稳定。")
        logger.info(f"你正在 {self._branch_name} 分支的 {self._commit_hash} 提交上。")


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
        return self._available

gitInfo = GitInfo()