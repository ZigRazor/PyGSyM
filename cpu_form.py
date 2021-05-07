import traceback
from asyncio import wait

from PyQt5.QtWidgets import QLineEdit
from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                            QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                            QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                            QVBoxLayout, QWidget, QFrame)
from qtpy.QtCore import QDateTime, Qt, QTimer, Slot, QThread, QObject, QRunnable, Signal
import psutil

import re

import CpuProgressBar


def set_progress_bar_value(progress_bar: QProgressBar, value: float):
    progress_bar.setValue(value)


class Cpu_Form(QDialog):

    def __init__(self, parent=None):
        super(Cpu_Form, self).__init__(parent)
        # Create widgets
        self.editFrequencyText = QLineEdit("1000")
        self.applyFrequency = QPushButton()
        self.frequencyLabel = QLabel()
        self.progressBarXcpu = []
        self.b_detail = QPushButton("ShowDetail")
        self.progressBar = CpuProgressBar.TotalCPUProgressBar()

        # Create Frame
        self.progressBar_x_cpu_frame = QFrame()

        # Create Layout
        self.frequencyLayout = QHBoxLayout()
        self.progressBar_x_cpu_Layout = QVBoxLayout()
        self.total_progressBarLayout = QHBoxLayout()
        self.layout = QVBoxLayout()

        # Other Classes
        self.data_grabber = CpuDataGrabber()
        self.thread = QThread()

        # self.setFrequency(100000.0)
        # self.timer = QTimer(self)

        self.create_frequency_handler()
        self.create_progress_bar_total()
        self.create_progress_bar_x_cpu()

        self.setLayout(self.layout)
        self.core_update_cpu_stat()

    def set_frequency(self, new_frequency: float):
        self.data_grabber.frequency = new_frequency

    def core_update_cpu_stat(self):
        self.data_grabber.moveToThread(self.thread)
        self.data_grabber.results.connect(self.update_cpu_stat)
        self.data_grabber.finished.connect(self.thread.quit)
        self.data_grabber.finished.connect(self.data_grabber.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.data_grabber.run)
        self.thread.start()

    def update_cpu_stat(self, results):
        value_total = results['value_total']
        value_x_cpu = results['value_x_cpu']
        cpu_count = results['cpu_count']

        for i in range(cpu_count):
            value_total += value_x_cpu[i]
            set_progress_bar_value(self.progressBarXcpu[i], value_x_cpu[i])
        value_total /= cpu_count
        set_progress_bar_value(self.progressBar, value_total)

    def total_cpu_progress_bar_update(self):
        set_progress_bar_value(self.progressBar, self.calculateCPUUsageTotal(self.frequency / 1000))

    def cpu_progress_bar_update_xcpu(self):
        x_cpu_usage = self.calculateCPUUsageXCPU(self.frequency / 1000)
        cpu_count = psutil.cpu_count()
        for i in range(cpu_count):
            set_progress_bar_value(self.progressBarXcpu[i], x_cpu_usage[i])

    def show_detail_clicked(self):
        if self.b_detail.isChecked():
            self.progressBar_x_cpu_frame.show()
            self.b_detail.setText("Hide Details")
        else:
            self.progressBar_x_cpu_frame.hide()
            self.b_detail.setText("Show Details")

    def create_progress_bar_total(self):
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

        label = QLabel()
        label.setText("Total")

        self.b_detail.setCheckable(True)
        self.b_detail.clicked.connect(self.show_detail_clicked)
        self.total_progressBarLayout.addWidget(label)
        self.total_progressBarLayout.addWidget(self.progressBar)
        self.total_progressBarLayout.addWidget(self.b_detail)
        self.layout.addLayout(self.total_progressBarLayout)

    def create_progress_bar_x_cpu(self):
        cpu_count = psutil.cpu_count()
        for i in range(cpu_count):
            self.progressBarXcpu.append(CpuProgressBar.XCPUProgressBar(None, i))
            self.progressBarXcpu[i].setRange(0, 100)
            self.progressBarXcpu[i].setValue(0)
            label = QLabel()
            label.setText("CPU " + str(i))
            internalLayout = QHBoxLayout()
            internalLayout.addWidget(label)
            internalLayout.addWidget(self.progressBarXcpu[i])
            self.progressBar_x_cpu_Layout.addLayout(internalLayout)
        self.progressBar_x_cpu_frame.setLayout(self.progressBar_x_cpu_Layout)
        self.progressBar_x_cpu_frame.hide()
        # layout.addLayout(self.progressBar_x_cpu_Layout)
        self.layout.addWidget(self.progressBar_x_cpu_frame)

        # timer = QTimer(self)
        # timer.timeout.connect(self.CPUProgressBarUpdateXCPU)
        # timer.start(1000)

    def update_frequency(self):
        value_string = re.search(r'\d+\.\d+|\d+', self.editFrequencyText.text())
        if value_string is not None:
            new_frequency = float(value_string.group())
            self.set_frequency(new_frequency)
            # self.setInterval(self.timer, new_frequency)

    def create_frequency_handler(self):
        self.frequencyLabel.setText("Set Frequency")
        self.applyFrequency.setText("Apply")
        self.applyFrequency.setGeometry(0, 0, 100, 50)

        self.applyFrequency.clicked.connect(self.update_frequency)

        self.frequencyLayout.addWidget(self.frequencyLabel)
        self.frequencyLayout.addWidget(self.editFrequencyText)
        self.frequencyLayout.addWidget(self.applyFrequency)
        self.layout.addLayout(self.frequencyLayout)


class CpuDataGrabber(QObject):
    finished = Signal()

    results = Signal(dict)  # set the type of object you are sending

    def __init__(self):
        super().__init__()
        self.cpu_count = psutil.cpu_count()
        self.value_x_cpu = 0
        self.value_total = 0.0
        self.frequency = 1000
        self.count = 0

    @staticmethod
    def calculate_usage_x_cpu(cpu_interval):
        return psutil.cpu_percent(interval=cpu_interval, percpu=True)

    def run(self):
        while True:
            try:
                self.value_x_cpu = self.calculate_usage_x_cpu(self.frequency / 1000)
                for i in range(self.cpu_count):
                    self.value_total += self.value_x_cpu[i]
                self.value_total /= self.cpu_count
                self.send_results()  # when done, send the results
            except:
                traceback.print_exc()

        self.finished.emit()

    def send_results(self):
        results = {'value_total': self.value_total, 'value_x_cpu': self.value_x_cpu, 'cpu_count': self.cpu_count}
        self.results.emit(results)
