from core.main import RPMain
import sys
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)

    instance = RPMain()

    app.setQuitOnLastWindowClosed(False)

    app.exec()
