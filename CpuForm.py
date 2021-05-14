from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                            QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QProgressBar, QPushButton,
                            QRadioButton, QScrollBar, QSizePolicy,
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


class CpuForm(QDialog):

    def __init__(self, parent=None):
        super(CpuForm, self).__init__(parent)
        # Create widgets
        self.editFrequencyText = QLineEdit("1000")
        self.applyFrequency = QPushButton()
        self.frequencyLabel = QLabel()
        self.progressBarXcpu = []

        # Create Frame
        self.cpu_total_frame = CpuFrame.CpuTotalFrame()
        self.cpu_x_cpu_frame = CpuFrame.CpuDetailedFrame()

        # Create Layout
        self.frequencyLayout = QHBoxLayout()
        self.progressBar_x_cpu_Layout = QVBoxLayout()
        self.layout = QVBoxLayout()

        # Other Classes
        self.cpu_percent_grabber = CpuDataGrabber.CpuPercentGrabber()
        self.thread_percent = QThread()
        self.cpu_times_grabber = CpuDataGrabber.CpuTimesGrabber()
        self.thread_times = QThread()

        self.create_frequency_handler()
        self.create_progress_bar_total()
        self.create_progress_bar_x_cpu()

        self.setLayout(self.layout)
        self.core_update_cpu_stat()

        self.cpu_total_frame.show_detail.connect(self.show_detail_clicked)

    def set_frequency(self, new_frequency: float):
        self.cpu_percent_grabber.frequency = new_frequency
        self.cpu_times_grabber.frequency = new_frequency

    def core_update_cpu_stat(self):
        # Percent
        self.cpu_percent_grabber.moveToThread(self.thread_percent)
        self.cpu_percent_grabber.results.connect(self.update_cpu_percent_stat)
        self.cpu_percent_grabber.finished.connect(self.thread_percent.quit)
        self.cpu_percent_grabber.finished.connect(self.cpu_percent_grabber.deleteLater)
        self.thread_percent.finished.connect(self.thread_percent.deleteLater)
        self.thread_percent.started.connect(self.cpu_percent_grabber.run)
        self.thread_percent.start()

        # Times
        self.cpu_times_grabber.moveToThread(self.thread_times)
        self.cpu_times_grabber.results.connect(self.update_cpu_times_stat)
        self.cpu_times_grabber.finished.connect(self.thread_times.quit)
        self.cpu_times_grabber.finished.connect(self.cpu_times_grabber.deleteLater)
        self.thread_times.finished.connect(self.thread_times.deleteLater)
        self.thread_times.started.connect(self.cpu_times_grabber.run)
        self.thread_times.start()

    def update_cpu_percent_stat(self, results):
        value_total = results['value_total']
        value_x_cpu = results['value_x_cpu']
        cpu_count = results['cpu_count']        
        self.cpu_total_frame.update_cpu_percent_stat(results)
        self.cpu_x_cpu_frame.update_cpu_percent_stat(results)

    def update_cpu_times_stat(self, results):
        value_total = results['value_total']
        value_x_cpu = results['value_x_cpu']
        cpu_count = results['cpu_count']
        self.cpu_total_frame.update_cpu_times_stat(results)
        self.cpu_x_cpu_frame.update_cpu_times_stat(results)

    def show_detail_clicked(self, show: bool):
        if show:
            self.cpu_x_cpu_frame.show()
        else:
            self.cpu_x_cpu_frame.hide()

    def create_progress_bar_total(self):
        self.layout.addWidget(self.cpu_total_frame)

    def create_progress_bar_x_cpu(self):
        self.layout.addWidget(self.cpu_x_cpu_frame)

    def update_frequency(self):
        value_string = re.search(r'\d+\.\d+|\d+', self.editFrequencyText.text())
        if value_string is not None:
            new_frequency = float(value_string.group())
            self.set_frequency(new_frequency)

    def create_frequency_handler(self):
        self.frequencyLabel.setText("Set Frequency")
        self.applyFrequency.setText("Apply")
        self.applyFrequency.setGeometry(0, 0, 100, 50)

        self.applyFrequency.clicked.connect(self.update_frequency)

        self.frequencyLayout.addWidget(self.frequencyLabel)
        self.frequencyLayout.addWidget(self.editFrequencyText)
        self.frequencyLayout.addWidget(self.applyFrequency)
        self.layout.addLayout(self.frequencyLayout)
