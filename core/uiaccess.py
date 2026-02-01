import ctypes
from ctypes import wintypes
from .config.dirs import DLL_DIR
import sys

# 加载 uiaccess.dll
# 确保 dll 文件在当前目录或系统路径中
try:
    uiaccess = ctypes.WinDLL(str(DLL_DIR / "uiaccess.dll"))
except OSError as e:
    print(f"Error: Could not load uiaccess.dll. {e}")
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

    print(f"Attempting to start: {command_line}")
    success = StartUIAccessProcess(
        app_name,
        command_line,
        flags,
        ctypes.byref(pid),
        session_id
    )

    if success:
        print(f"Successfully started process with PID: {pid.value}")
        return pid.value
    else:
        error_code = ctypes.get_last_error()
        print(f"Failed to start process. Error code: {error_code}")
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
        print("This script must be run as Administrator.")
        sys.exit(1)

    if IsUIAccess():
        print("Current process is already running with UIAccess.")
    else:
        print("Current process is NOT running with UIAccess.")

    # 示例：启动记事本
    target_command = "notepad.exe"
    run_with_uiaccess(target_command)
