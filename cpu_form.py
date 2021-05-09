from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                            QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                            QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                            QVBoxLayout, QWidget, QFrame, QLineEdit)
from qtpy.QtCore import QDateTime, Qt, QTimer, Slot, QThread, QObject, QRunnable, Signal
import psutil

import re

import CpuProgressBar
import CpuDataGrabber
import CpuFrame


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
        #self.b_detail = QPushButton("ShowDetail")
        #self.progressBar = CpuProgressBar.TotalCPUProgressBar()
        #self.label_total_cpu = QLabel()

        # Create Frame
        self.progressBar_total_frame = CpuFrame.CpuTotalFrame()
        self.progressBar_x_cpu_frame = QFrame()

        # Create Layout
        self.frequencyLayout = QHBoxLayout()
        self.progressBar_x_cpu_Layout = QVBoxLayout()
        #self.total_progressBarLayout = QHBoxLayout()
        self.layout = QVBoxLayout()

        # Other Classes
        self.data_grabber = CpuDataGrabber.CpuDataGrabber()
        self.thread = QThread()

        # self.setFrequency(100000.0)
        # self.timer = QTimer(self)

        self.create_frequency_handler()
        self.create_progress_bar_total()
        self.create_progress_bar_x_cpu()

        self.setLayout(self.layout)
        self.core_update_cpu_stat()

        self.progressBar_total_frame.show_detail.connect(self.show_detail_clicked)

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
        self.progressBar_total_frame.update_cpu_stat(results)

    def show_detail_clicked(self, show: bool):
        if show:
            self.progressBar_x_cpu_frame.show()
        else:
            self.progressBar_x_cpu_frame.hide()

    def create_progress_bar_total(self):
        self.layout.addWidget(self.progressBar_total_frame)

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
