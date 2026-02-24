import sys

from PySide6.QtWidgets import QApplication
from loguru import logger

from core.config.dirs import ROOT
from core.main import RPMain

logger.add(str(ROOT / "logs/RandPicker-{time:YYYY-MM-DD}.log"), rotation="00:00")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    instance = RPMain()

    app.setQuitOnLastWindowClosed(False)

    app.exec()
