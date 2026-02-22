"""UI Access"""

# --*--
# DLL 来源于 https://github.com/shc0743/RunUIAccess
# 实现中参考了 shc0743 的部分代码。
# 部分代码由 AI 编写。
# --*--

import ctypes
import sys
from ctypes import wintypes

from loguru import logger

from .config.dirs import DLL_DIR

# 加载 uiaccess.dll
# 确保 dll 文件在当前目录或系统路径中
try:
    uiaccess = ctypes.WinDLL(str(DLL_DIR / "uiaccess.dll"))
except OSError as e:
    logger.error(f"加载 uiaccess.dll 时出错: {e}")
    sys.exit(1)

# 定义 StartUIAccessProcess 函数原型
# BOOL WINAPI StartUIAccessProcess(LPCWSTR appName, PCWSTR cmdLine, DWORD flag, PDWORD pPid, DWORD dwSession);
StartUIAccessProcess = uiaccess.StartUIAccessProcess
StartUIAccessProcess.argtypes = [
    wintypes.LPCWSTR,  # appName
    wintypes.LPCWSTR,  # cmdLine
    wintypes.DWORD,  # flag
    ctypes.POINTER(wintypes.DWORD),  # pPid
    wintypes.DWORD  # dwSession
]
StartUIAccessProcess.restype = wintypes.BOOL

# 定义 IsUIAccess 函数原型
# BOOL WINAPI IsUIAccess();
IsUIAccess = uiaccess.IsUIAccess
IsUIAccess.argtypes = []
IsUIAccess.restype = wintypes.BOOL


def run_with_uiaccess(command_line, app_name=None):
    """
    使用 UIAccess 权限启动进程
    """
    pid = wintypes.DWORD(0)

    # 获取当前会话 ID
    # 通常使用 WTSGetActiveConsoleSessionId 获取当前活动的控制台会话
    kernel32 = ctypes.WinDLL("kernel32")
    WTSGetActiveConsoleSessionId = kernel32.WTSGetActiveConsoleSessionId
    WTSGetActiveConsoleSessionId.restype = wintypes.DWORD

    session_id = WTSGetActiveConsoleSessionId()

    # 标志位，通常设为 0 即可，底层会自动添加 CREATE_NEW_CONSOLE
    flags = 0

    logger.debug(f"即将启动: {command_line}")
    success = StartUIAccessProcess(
        app_name,
        command_line,
        flags,
        ctypes.byref(pid),
        session_id
    )

    if success:
        logger.success(f"成功启动进程。PID: {pid.value}")
        return pid.value
    else:
        error_code = ctypes.get_last_error()
        logger.exception(f"启动进程失败。错误代码: {error_code}")
        return None


def check_privileges():
    """
    检查当前是否具有管理员权限
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


if __name__ == "__main__":
    if not check_privileges():
        logger.warning("必须用管理员权限运行。")
        sys.exit(1)

    if IsUIAccess():
        logger.info("当前进程已具有 UIAccess")
    else:
        logger.info("当前进程不具有 UIAccess")

    # 示例：启动记事本
    target_command = "notepad.exe"
    run_with_uiaccess(target_command)
