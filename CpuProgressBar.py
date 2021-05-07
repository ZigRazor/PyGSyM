from qtpy.QtWidgets import QProgressBar
from qtpy.QtGui import QMouseEvent

class TotalCPUProgressBar(QProgressBar):
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
         print("Total CPU")

class XCPUProgressBar(QProgressBar):

    def __init__(self, parent, id : int):
        super().__init__(parent)
        self.uid = id

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
         print("X CPU " + str(self.uid))