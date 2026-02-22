"""
向 ClassIsland 发送通知

"""
import asyncio
import sys
import threading
import time
from collections import deque
from typing import Optional

from PySide6.QtCore import QObject, Slot, Signal
from loguru import logger

from ..config.dirs import DLL_DIR

CSHARP_AVAILABLE = False
try:
    # raise Exception("Test")
    from pythonnet import load

    try:
        runtime_config = DLL_DIR / "randpicker.runtimeconfig.json"
        load("coreclr", runtime_config=str(runtime_config))
    except Exception:
        logger.exception("加载 .NET Core 失败，检查是否安装 .NET Core 运行时 8.0。")
        raise Exception

    import clr

    sys.path.append(DLL_DIR.as_posix())
    clr.AddReference("RP4CI.Interface")
    clr.AddReference("ClassIsland.Shared.IPC")

    from System.Collections.Generic import List

    from ClassIsland.Shared.IPC import IpcClient
    from dotnetCampus.Ipc.CompilerServices.GeneratedProxies import GeneratedIpcFactory
    from RP4CI.Interface.Models import NotifyResult, PickType, OverlayType, PickStudent, CustomProperty
    from RP4CI.Interface.Services import IRPService

    CSHARP_AVAILABLE = True
    logger.success("成功加载 ClassIsland 集成所需库。")

except Exception as e:
    logger.error(f"加载 ClassIsland 集成库时发生错误: {e}")
    logger.warning("ClassIsland 集成在您的系统上不可用，即使您能在设置中启用它。")

if CSHARP_AVAILABLE:
    class ClassIslandIntegration(QObject):
        connectivityUpdated = Signal(str)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.main = None
            self.settingsConfig = None
            self.is_available = CSHARP_AVAILABLE
            self.connectivity_status: str = "NotRunning"

            self.ipcClient: Optional[IpcClient] = None
            self.client_thread: Optional[threading.Thread] = None
            self.event_loop: Optional[asyncio.AbstractEventLoop] = None
            self._client_task: Optional[asyncio.Task] = None
            self._set_connectivity("NotRunning")
            self.is_running = False
            self.reconnect_attempts = deque()

        def _set_connectivity(self, status: str):
            if self.connectivity_status == status:
                return
            self.connectivity_status = status
            self.connectivityUpdated.emit(status)

        @Slot(result=str)
        def get_connectivity_status(self) -> str:
            return self.connectivity_status

        def start(self):
            if self.is_running:
                return
            if not self.is_available:
                self._set_connectivity("NotRunning")
                return
            try:
                self._set_connectivity("NotConnected")
                self.client_thread = threading.Thread(target=self._run, daemon=False)
                self.client_thread.start()
                logger.info("ClassIsland 集成客户端已启动。")
                self.is_running = True
            except Exception as e:
                logger.error(f"启动 ClassIsland 集成客户端时出错: {e}")
                self.is_running = False

        def stop(self):
            self.is_running = False
            try:
                if self.event_loop and self.event_loop.is_running():
                    def _cancel_client_task():
                        if self._client_task and not self._client_task.done():
                            self._client_task.cancel()

                    self.event_loop.call_soon_threadsafe(_cancel_client_task)
                if self.client_thread and self.client_thread.is_alive():
                    self.client_thread.join(timeout=5)
                logger.info("ClassIsland 集成客户端已停止。")
            except Exception as e:
                logger.exception(e)

        def _run(self):
            async def client():
                self.ipcClient = IpcClient()

                # 预留 注册事件处理器

                while self.is_running:
                    await asyncio.sleep(1)
                    # 实时检查连接状态
                    if not self._check_alive():
                        # 连接重试
                        if len(self.reconnect_attempts) != 0:  # 当非首次失连时 (REAL 失联)
                            self._set_connectivity("NotConnected")
                            logger.warning("ClassIsland 集成客户端连接丢失，正在尝试重新连接...")
                            if not self._allow_reconnect():
                                logger.warning("重连频率太大，本次启动停止重连。")
                                logger.info("检查是否已经安装 RandPicker 插件。")
                                self.is_running = False
                                self._stop_event_loop()
                                self._set_connectivity("NotRunning")
                                break
                        else:  # 首次连接 不是“连接丢失”
                            self._allow_reconnect()  # 让队列里保留一个首次连接的尝试

                        task = self.ipcClient.Connect()
                        await self._await_dotnet_task(task)
                        self._set_connectivity("Connected")
                        logger.info("ClassIsland 集成客户端已连接。")

            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            try:
                self._client_task = self.event_loop.create_task(client())
                self.event_loop.run_until_complete(self._client_task)
            except Exception as e:
                logger.exception(f"ClassIsland 集成客户端运行时出错: {e}")
            except asyncio.CancelledError:
                pass
            finally:
                self._cleanup()

        async def _await_dotnet_task(self, task):
            loop = asyncio.get_running_loop()
            done = loop.create_future()

            def _worker():
                try:
                    task.Wait()
                except Exception as exc:
                    loop.call_soon_threadsafe(done.set_exception, exc)
                else:
                    loop.call_soon_threadsafe(done.set_result, None)

            threading.Thread(target=_worker, daemon=True).start()
            await done

        def _cleanup(self):
            self._client_task = None
            self.event_loop.close()
            self.event_loop = None
            self._set_connectivity("NotRunning")

        def _stop_event_loop(self):
            if self.event_loop and self.event_loop.is_running():
                self.event_loop.call_soon_threadsafe(self.event_loop.stop)

        def _allow_reconnect(self) -> bool:
            now = time.monotonic()
            cutoff = now - 10
            while self.reconnect_attempts and self.reconnect_attempts[0] < cutoff:
                self.reconnect_attempts.popleft()
            if len(self.reconnect_attempts) >= 3:
                return False
            self.reconnect_attempts.append(now)
            return True

        def _check_alive(self) -> bool:
            try:
                rpService = GeneratedIpcFactory.CreateIpcProxy[IRPService](self.ipcClient.Provider,
                                                                           self.ipcClient.PeerProxy)
                return rpService.PingService() == "Pong"
            except Exception:
                # 好吵 删了
                # logger.warning(f"检查 ClassIsland 集成连接状态时出现 {type(e)} 错误: {e}")
                return False

        def send_message(self, pick_type: str, stus: list) -> bool:
            if self.connectivity_status != "Connected":
                logger.warning("ClassIsland 未连接或未运行，无法发送通知。")
                return False
            try:
                result = self._format_message(pick_type, stus)
                self._send(result)
                return True
            except Exception as e:
                logger.exception(f"发送 ClassIsland 通知时出错: {e}")
                return False

        def send_test(self):
            if self.connectivity_status != "Connected":
                logger.warning("ClassIsland 未连接或未运行，无法发送测试通知。")
                return False
            try:
                result = NotifyResult()
                result.PickType = PickType.Test
                result.Title = "测试通知"
                result.Overlay = "这是一条来自 RandPicker 的测试通知。"
                self._send(result)
            except Exception as e:
                logger.exception(f"发送 ClassIsland 测试通知时出错: {e}")
                return False

        def _format_message(self, pick_type: str, stus: list) -> NotifyResult:
            """对通知进行前处理"""
            result = NotifyResult()

            format = self.settingsConfig.getNotifyFormat("classisland")

            names = format['names']['separator'].join([s.get("name", "未知") for s in stus])
            count = len(stus)
            suffix = format['suffix']['person'] if pick_type == "person" else format['suffix']['group']

            title_template = format['title']
            body_template = format['body']

            result.Title = title_template.replace("{count}", str(count)).replace("{suffix}", suffix).replace("{names}",
                                                                                                             names)
            result.Overlay = body_template.replace("{count}", str(count)).replace("{suffix}", suffix).replace("{names}",
                                                                                                              names)

            result.PickType = PickType.Person if pick_type == "person" else PickType.Group
            result.TitleDuration = self.settingsConfig.getCiMaskDuration()
            result.OverlayDuration = self.settingsConfig.getCiOverlayDuration()

            if pick_type == "person":
                result.StudentList = List[PickStudent]()
                for stu in stus:
                    pick_stu = PickStudent()
                    pick_stu.Name = stu.get("name", "未知")
                    pick_stu.Weight = stu.get("weight", 1)
                    pick_stu.CustomProperties = List[CustomProperty]()
                    for p in stu.get("properties", []):
                        custom_property = CustomProperty()
                        custom_property.Name = p.get("name", "")
                        custom_property.Value = p.get("value", "")
                        pick_stu.CustomProperties.Add(custom_property)
                    result.StudentList.Add(pick_stu)
            elif pick_type == "group":
                # TODO)) GROUP
                pass
            else:
                pass

            overlayType = self.settingsConfig.getCiOverlayType()
            match overlayType:
                case "simple":
                    result.OverlayType = OverlayType.Simple
                case "rolling":
                    result.OverlayType = OverlayType.Rolling
                case "auto":
                    # TODO)) 自动检测
                    result.OverlayType = OverlayType.Simple
                case _:
                    result.OverlayType = OverlayType.Simple

            return result

        def _send(self, result: NotifyResult):
            """
            发送通知到 ClassIsland

            :param result: 由 _format_message 生成的 NotifyResult
            """
            try:
                rpService = GeneratedIpcFactory.CreateIpcProxy[IRPService](self.ipcClient.Provider,
                                                                           self.ipcClient.PeerProxy)
                rpService.Notify(result)
                logger.success(f"ClassIsland 通知发送成功: {result.Title}: {result.Overlay}")
            except Exception as e:
                logger.error(f"向 ClassIsland 发送通知时出错: {e}")

        def get_availability(self):
            return self.is_available
# 不是怎么老被炸啊（
else:
    class ClassIslandIntegration(QObject):
        connectivityUpdated = Signal(str)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.is_available = False
            self.connectivity_status = "NotAvailable"

        @Slot(result=str)
        def get_connectivity_status(self) -> str:
            return self.connectivity_status

        def start(self):
            logger.warning("ClassIsland 集成不可用，无法启动客户端。")

        def send_message(self, pick_type: str, stus: list) -> bool:
            logger.warning("ClassIsland 集成不可用，无法发送通知。")
            return False

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
