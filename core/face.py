"""
人脸抽选模块
"""
import platform
import random
from pathlib import Path
from typing import Optional

import cv2
from PySide6.QtCore import QObject, Slot, Signal, QTimer
from PySide6.QtGui import QImage
from PySide6.QtQuick import QQuickImageProvider
from loguru import logger

from .config.dirs import ASSETS_DIR


class CameraImageProvider(QQuickImageProvider):
    """为 QML 提供摄像头帧的 ImageProvider"""

    def __init__(self):
        super().__init__(QQuickImageProvider.ImageType.Image)
        self._image = QImage(640, 480, QImage.Format.Format_RGB888)
        self._image.fill(0)

    def requestImage(self, id, size, requestedSize):
        if self._image is not None:
            return self._image
        return QImage()

    def updateImage(self, image: QImage):
        self._image = image


class FaceImageProvider(QQuickImageProvider):
    """为 QML 提供人脸抠图的内存 ImageProvider，避免将生物特征图像写入磁盘"""

    def __init__(self):
        super().__init__(QQuickImageProvider.ImageType.Image)
        self._images: dict[str, QImage] = {}

    def requestImage(self, id, size, requestedSize):
        img = self._images.get(id)
        if img is not None:
            return img
        return QImage()

    def store(self, key: str, image: QImage):
        self._images[key] = image

    def clear(self):
        self._images.clear()


class FaceChooser(QObject):
    """人脸抽选"""
    _instance: "FaceChooser" = None

    frameReady = Signal()
    cameraStatusChanged = Signal(str)

    @classmethod
    def instance(cls) -> "FaceChooser":
        return cls._instance

    def __init__(self, parent=None):
        super().__init__(parent)
        FaceChooser._instance = self

        self._capture: Optional[cv2.VideoCapture] = None
        self._current_frame = None
        self._camera_id = 0  # int index or str device path
        self._is_running = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._grab_frame)

        self.imageProvider = CameraImageProvider()
        self.faceImageProvider = FaceImageProvider()

        # 加载 YuNet 人脸检测模型
        model_path = str(ASSETS_DIR / "face_detection_yunet_2023mar.onnx")
        self._face_detector = None
        try:
            self._face_detector = cv2.FaceDetectorYN.create(
                model_path, "", (320, 320), 0.9, 0.3, 5000
            )
        except Exception as e:
            logger.error(f"无法加载人脸检测模型: {e}")

        logger.info("人脸抽选模块已初始化（YuNet）")

    @staticmethod
    def _get_linux_video_devices() -> list[dict]:
        """通过 /sys/class/video4linux 获取实际存在的视频捕获设备"""
        devices = []
        v4l_dir = Path("/sys/class/video4linux")
        if v4l_dir.is_dir():
            for entry in v4l_dir.iterdir():
                dev_name = entry.name  # e.g. "video0"
                if not dev_name.startswith("video"):
                    continue
                # 只保留每个物理设备的第一个节点（index=0 是视频捕获，index=1 通常是元数据）
                node_index_path = entry / "index"
                if node_index_path.exists():
                    try:
                        node_index = int(node_index_path.read_text().strip())
                        if node_index != 0:
                            continue
                    except (OSError, ValueError):
                        pass
                dev_path = f"/dev/{dev_name}"
                # 获取设备名称
                name = None
                name_path = entry / "name"
                if name_path.exists():
                    try:
                        name = name_path.read_text().strip()
                    except OSError:
                        pass
                devices.append({"path": dev_path, "name": name or dev_name})
        devices.sort(key=lambda d: d["path"])
        return devices

    @Slot(result=list)
    def getAvailableCameras(self) -> list:
        """枚举可用的摄像头，返回真实设备名称"""
        cameras = []
        is_linux = platform.system() == "Linux"

        if is_linux:
            for dev in self._get_linux_video_devices():
                # 使用设备路径 + V4L2 后端直接打开，避免 FFMPEG 等后端报错
                cap = cv2.VideoCapture(dev["path"], cv2.CAP_V4L2)
                if cap.isOpened():
                    cameras.append({"id": dev["path"], "name": dev["name"]})
                cap.release()
        else:
            # Windows / macOS: 先用 cv2 探测，得到经过验证的索引列表；
            # 再用 QMediaDevices 获取真实名称。两者基于相同的底层 OS API
            # （Windows: MSMF/DirectShow；macOS: AVFoundation），枚举顺序一致。
            # 只有计数吻合时才将名称与索引配对，避免因排序差异对应到错误设备。
            cv_indices = []
            for i in range(10):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    cv_indices.append(i)
                cap.release()

            qt_names = self._get_qt_camera_names()
            if qt_names and len(qt_names) == len(cv_indices):
                # 数量吻合：按顺序配对，使用 Qt 提供的真实设备名称
                for idx, name in zip(cv_indices, qt_names):
                    cameras.append({"id": idx, "name": name})
            else:
                # 数量不一致或 Qt 不可用：使用已验证的 cv2 索引，名称回退为通用格式
                for i in cv_indices:
                    cameras.append({"id": i, "name": f"Camera {i}"})
        return cameras

    @staticmethod
    def _get_qt_camera_names() -> list[str]:
        """通过 PySide6 QMediaDevices 获取摄像头真实名称列表"""
        try:
            from PySide6.QtMultimedia import QMediaDevices
            return [d.description() for d in QMediaDevices.videoInputs()]
        except Exception:
            return []

    @Slot(str)
    def switchCamera(self, camera_id):
        """切换到另一个摄像头（camera_id 可以是设备路径或数字索引）"""
        was_running = self._is_running
        if self._is_running:
            self.stopCamera()
        # 尝试转为 int（Windows 等平台），否则保持为设备路径字符串
        try:
            self._camera_id = int(camera_id)
        except (ValueError, TypeError):
            self._camera_id = camera_id
        if was_running:
            self.startCamera()

    @Slot()
    def startCamera(self):
        """启动摄像头"""
        if self._is_running:
            return
        if isinstance(self._camera_id, str):
            self._capture = cv2.VideoCapture(self._camera_id, cv2.CAP_V4L2)
        else:
            self._capture = cv2.VideoCapture(self._camera_id)
        if not self._capture.isOpened():
            logger.error(f"无法打开摄像头 {self._camera_id}")
            self._capture.release()
            self._capture = None
            self.cameraStatusChanged.emit("error")
            return
        self._is_running = True
        self._timer.start(33)  # ~30 FPS
        self.cameraStatusChanged.emit("running")
        logger.info(f"摄像头 {self._camera_id} 已开启")

    @Slot()
    def stopCamera(self):
        """停止摄像头"""
        self._timer.stop()
        self._is_running = False
        if self._capture:
            self._capture.release()
            self._capture = None
        self.cameraStatusChanged.emit("stopped")
        logger.info("摄像头已关闭")

    @Slot(result=bool)
    def isCameraRunning(self) -> bool:
        """摄像头是否正在运行"""
        return self._is_running

    def _grab_frame(self):
        """从摄像头获取一帧"""
        if self._capture and self._capture.isOpened():
            ret, frame = self._capture.read()
            if ret:
                self._current_frame = frame
                # 转换为 QImage
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytes_per_line = ch * w
                qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()
                self.imageProvider.updateImage(qimg)
                self.frameReady.emit()

    @Slot(int, result=list)
    def captureAndDetect(self, count: int = 1) -> list:
        """拍照并检测人脸，随机选择 count 张人脸"""
        if self._current_frame is None:
            logger.warning("没有可用的摄像头帧")
            return []
        if self._face_detector is None:
            logger.error("人脸检测模型未加载")
            return []

        frame = self._current_frame.copy()
        h, w = frame.shape[:2]

        # 设置检测器输入尺寸并检测
        self._face_detector.setInputSize((w, h))
        _, faces = self._face_detector.detect(frame)

        if faces is None or len(faces) == 0:
            logger.info("未检测到人脸")
            return []

        logger.info(f"检测到 {len(faces)} 张人脸")

        # 随机选择
        face_list = list(faces)
        if count > len(face_list):
            count = len(face_list)
        selected = random.sample(face_list, count)

        # 清除上一轮缓存，将新抠图存入内存 Provider，不写入磁盘
        self.faceImageProvider.clear()

        results = []
        for i, face in enumerate(selected):
            # YuNet 返回 [x, y, w, h, ...landmarks..., score]
            fx, fy, fw, fh = int(face[0]), int(face[1]), int(face[2]), int(face[3])

            # 添加边距
            pad = int(max(fw, fh) * 0.25)
            x1 = max(0, fx - pad)
            y1 = max(0, fy - pad)
            x2 = min(w, fx + fw + pad)
            y2 = min(h, fy + fh + pad)

            face_crop = frame[y1:y2, x1:x2]

            # 转为 QImage 存入内存 Provider；生物特征图像不落盘
            rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
            crop_h, crop_w = rgb.shape[:2]
            qimg = QImage(
                rgb.data, crop_w, crop_h, crop_w * 3, QImage.Format.Format_RGB888
            ).copy()
            key = f"face_{i}"
            self.faceImageProvider.store(key, qimg)

            results.append({
                "path": f"image://faces/{key}",
                "x": fx,
                "y": fy,
                "width": fw,
                "height": fh,
                "index": i
            })

        logger.info(f"随机选择了 {len(results)} 张人脸")
        return results

    @Slot(result=int)
    def detectFaceCount(self) -> int:
        """检测当前帧中的人脸数量"""
        if self._current_frame is None or self._face_detector is None:
            return 0
        h, w = self._current_frame.shape[:2]
        self._face_detector.setInputSize((w, h))
        _, faces = self._face_detector.detect(self._current_frame)
        return len(faces) if faces is not None else 0

    def cleanup(self):
        """清理资源"""
        self.stopCamera()
        self.faceImageProvider.clear()
