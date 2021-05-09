from qtpy.QtWidgets import QProgressBar
from qtpy.QtGui import QMouseEvent
from qtpy.QtCore import Signal


class TotalCPUProgressBar(QProgressBar):
    clicked = Signal()

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        print("Total CPU")
        self.clicked.emit()


class XCPUProgressBar(QProgressBar):
    clicked = Signal()

    def __init__(self, parent, id: int):
        super().__init__(parent)
        self.uid = id

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        print("X CPU " + str(self.uid))
        self.clicked.emit()
