from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                            QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QProgressBar, QPushButton,
                            QRadioButton, QScrollBar, QSizePolicy,
                            QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                            QVBoxLayout, QWidget, QFrame, QLineEdit)
from qtpy.QtCore import QDateTime, Qt, QTimer, Slot, QThread, QObject, QRunnable, Signal
from qtpy.QtGui import QMouseEvent
import psutil


class CpuTotalFrame(QFrame):
    show_detail = Signal(bool)

    def __init__(self):
        super().__init__()
        # widget
        self.label_test = QLabel("test")
        self.button_test = QPushButton("test")
        self.pb_total_cpu = QProgressBar()
        self.l_total_cpu = QLabel()
        self.b_detail = QPushButton("ShowDetail")

        # layout
        self.lay_total_cpu = QHBoxLayout()

        # initialize
        self.pb_total_cpu.setRange(0, 100)
        self.pb_total_cpu.setValue(0)
        self.l_total_cpu.setText("Total")

        self.b_detail.setCheckable(True)
        self.b_detail.clicked.connect(self.show_detail_clicked)
        self.lay_total_cpu.addWidget(self.l_total_cpu)
        self.lay_total_cpu.addWidget(self.pb_total_cpu)
        self.lay_total_cpu.addWidget(self.b_detail)
        self.setLayout(self.lay_total_cpu)
        # self.layout.addWidget(self.progressBar_total_frame)

    def switch_progress_bar_total(self):

        if self.pb_total_cpu.isHidden():
            self.lay_total_cpu.replaceWidget(self.labelMio, self.pb_total_cpu)
            self.lay_total_cpu.replaceWidget(self.button_pippo, self.b_detail)
            self.labelMio.hide()
            self.button_pippo.hide()
            self.pb_total_cpu.show()
            self.b_detail.show()
        else:
            self.lay_total_cpu.replaceWidget(self.pb_total_cpu, self.label_test)
            self.lay_total_cpu.replaceWidget(self.b_detail, self.button_test)
            self.label_test.show()
            self.button_test.show()
            self.pb_total_cpu.hide()
            self.b_detail.hide()

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        print("mouse release event")
        self.switch_progress_bar_total()

    def show_detail_clicked(self):
        if self.b_detail.isChecked():
            self.show_detail.emit(True)
            self.b_detail.setText("Hide Details")
        else:
            self.show_detail.emit(False)
            self.b_detail.setText("Show Details")

    def update_cpu_stat(self, stats):
        value_total = stats['value_total']
        value_x_cpu = stats['value_x_cpu']
        cpu_count = stats['cpu_count']
        for i in range(cpu_count):
            value_total += value_x_cpu[i]
        value_total /= cpu_count
        self.pb_total_cpu.setValue(value_total)
