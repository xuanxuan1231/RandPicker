"""
向 ClassIsland 发送通知

"""
import os
import sys
from typing import Optional
import asyncio

from PySide6.QtCore import QObject, Slot, Signal
from loguru import logger
import threading
from ..config.dirs import DLL_DIR

CSHARP_AVAILABLE = False
try:
    # import clr
    from pythonnet import load

    load("coreclr")
    import clr

    sys.path.append(DLL_DIR.as_posix())
    clr.AddReference("RP4CI.Shared")
    clr.AddReference("ClassIsland.Shared.IPC")


    from ClassIsland.Shared.IPC import IpcClient
    from dotnetCampus.Ipc.CompilerServices.GeneratedProxies import GeneratedIpcFactory
    from dotnetCampus.Ipc.Exceptions import IpcPeerConnectionBrokenException
    from RP4CI.Shared.Models import NotifyResult, PickType, OverlayType
    from RP4CI.Shared.Services import IRPService


    CSHARP_AVAILABLE = True
    logger.success("成功加载 ClassIsland 集成所需库。")

except Exception as e:
    logger.error(f"加载 ClassIsland 集成库时发生错误: {e}")
    logger.warning("ClassIsland 集成在您的系统上不可用。")


class ClassIslandIntegration(QObject):
    connectivityUpdated = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_available = CSHARP_AVAILABLE
        self.is_connected: bool = False

        self.ipcClient: Optional[IpcClient] = None
        self.client_thread: Optional[threading.Thread] = None
        self.event_loop: Optional[asyncio.AbstractEventLoop] = None
        self._set_connectivity(False)
        self.is_running = False

    def _set_connectivity(self, connected: bool):
        if self.is_connected == connected:
            return
        self.is_connected = connected
        self.connectivityUpdated.emit(connected)

    @Slot(result=bool)
    def get_connectivity_status(self) -> bool:
        return self.is_connected

    def start(self):
        if self.is_running:
            return
        if not self.is_available:
            self._set_connectivity(False)
            return
        try:
            self.client_thread = threading.Thread(target=self._run, daemon=True)
            self.client_thread.start()
            logger.info("ClassIsland 集成客户端已启动。")
            self.is_running = True
        except Exception as e:
            logger.error(f"启动 ClassIsland 集成客户端时出错: {e}")
            self.is_running = False

    def _run(self):
        async def client():
            self.ipcClient = IpcClient()

            # 预留 注册事件处理器

            task = self.ipcClient.Connect()
            await self.event_loop.run_in_executor(None, task.Wait)
            self._set_connectivity(True)
            logger.info("ClassIsland 集成客户端已连接。")

            while self.is_running:
                await asyncio.sleep(1)
                # 实时检查连接状态
                if self._check_alive():
                    continue
                else:
                    self._set_connectivity(False)
                    logger.warning("ClassIsland 集成客户端连接丢失，正在尝试重新连接...")

                    task = self.ipcClient.Connect()
                    await self.event_loop.run_in_executor(None, task.Wait)
                    self._set_connectivity(True)
                    logger.info("ClassIsland 集成客户端已重新连接。")

        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)
        try:
            self.event_loop.run_until_complete(client())
        except Exception as e:
            logger.exception(f"ClassIsland 集成客户端运行时出错: {e}")
        finally:
            self.event_loop.close()
            self.event_loop = None
            self._set_connectivity(False)

    def _check_alive(self) -> bool:
        try:
            rpService = GeneratedIpcFactory.CreateIpcProxy[IRPService](self.ipcClient.Provider, self.ipcClient.PeerProxy)
            return rpService.PingService() == "Pong"
        except Exception:
            # 好吵 删了
            # logger.warning(f"检查 ClassIsland 集成连接状态时出现 {type(e)} 错误: {e}")
            return False

    def send_message(self, pick_type: str, stus: list) -> bool:
        try:
            result = self._format_message(pick_type, stus)
            self._send(result)
            return True
        except Exception as e:
            logger.exception(f"发送 ClassIsland 通知时出错: {e}")
            return False

    @staticmethod
    def _format_message(pick_type: str, stus: list) -> NotifyResult:
        result = NotifyResult()
        result.PickType = PickType.Person if pick_type == "person" else PickType.Group

        # TODO)) 这里本应从设置中读取，但是先这样吧（
        result.Title = f"抽选了 {len(stus)} " + ("名学生" if pick_type == "person" else "个小组")
        result.Overlay = ", ".join(stus)

        return result

    def _send(self, result: NotifyResult):
        """
        发送通知到 ClassIsland

        :param result: 由 _format_message 生成的 NotifyResult
        """
        try:
            rpService = GeneratedIpcFactory.CreateIpcProxy[IRPService](self.ipcClient.Provider, self.ipcClient.PeerProxy)
            rpService.Notify(result)
            logger.success(f"ClassIsland 通知发送成功: {result.Title}: {result.Overlay}")
        except Exception as e:
            logger.error(f"向 ClassIsland 发送通知时出错: {e}")

    def get_availability(self):
        return self.is_available

ciService = ClassIslandIntegration()

def initialize_ci_service():
    global ciService
    try:
        ciService.start()
    except Exception as e:
        logger.error(f"初始化 ClassIsland 集成服务时出错: {e}")

initialize_ci_service()
