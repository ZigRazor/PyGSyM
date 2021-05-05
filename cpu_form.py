import traceback
from asyncio import wait

from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                            QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                            QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                            QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                            QVBoxLayout, QWidget, QFrame)
from qtpy.QtCore import QDateTime, Qt, QTimer, Slot, QThread, QObject, Signal, QRunnable
from PyQt5.QtCore import pyqtSignal,pyqtSlot
import psutil

import re


class Cpu_Form(QDialog):

    def __init__(self, parent=None):
        super(Cpu_Form, self).__init__(parent)
        # Create widgets
                
        # Create layout and add widgets
        layout = QVBoxLayout()        

        self.setFrequency(100000.0)
        self.timer = QTimer(self)
                       
        self.createFrequencyHandler(layout)
        self.createProgressBarTotal(layout)
        self.createProgressBarXCPU(layout)

        #self.timer.timeout.connect(self.core_updateCpuStat)
        #self.timer.start(100000)
        #self.setInterval(self.timer,self.frequency/1000)
        #self.button = QPushButton('Run')
        #self.button.clicked.connect(self.core_updateCpuStat)
        #layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        self.core_updateCpuStat()

    def setFrequency(self, new_frequency: float):
        self.frequency = new_frequency
    
    def setInterval(self, timer, newInterval):
        timer.setInterval(newInterval)

    def core_updateCpuStat(self):
        self.thread = QThread()
        self.data_grabber = DataGrabber()
        self.data_grabber.moveToThread(self.thread)
        self.data_grabber.results.connect(self.updateCpuStat)
        #self.data_grabber.finished.connect(self.complete)
        self.data_grabber.finished.connect(self.thread.quit)
        self.data_grabber.finished.connect(self.data_grabber.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.data_grabber.run)
        self.thread.start()


    def updateCpuStat(self, results):
        value_total = results['value_total']
        value_x_cpu = results['value_x_cpu']
        cpu_count = results['cpu_count']

        for i in range(cpu_count):
            value_total += value_x_cpu[i]
            self.setProgressBarValue(self.progressBarXcpu[i], value_x_cpu[i])
        value_total /= cpu_count
        self.setProgressBarValue(self.progressBar, value_total)

    def setProgressBarValue(self, progressBar : QProgressBar, value : float):
        progressBar.setValue(value)

    def calculateCPUUsageTotal(self, cpu_interval):
        return psutil.cpu_percent(interval=cpu_interval)



    def totalCCPUProgressBarUpdate(self):
        self.setProgressBarValue(self.progressBar ,self.calculateCPUUsageTotal(self.frequency/1000))

    def CPUProgressBarUpdateXCPU(self):
        x_cpu_usage = self.calculateCPUUsageXCPU(self.frequency/1000)
        cpu_count = psutil.cpu_count()
        for i in range (cpu_count):
            self.setProgressBarValue(self.progressBarXcpu[i] ,x_cpu_usage[i])

    def show_detail_clicked(self):
        if self.b_detail.isChecked():
            self.progressBar_x_cpu_frame.show()
            self.b_detail.setText("Hide Details")
        else:
            self.progressBar_x_cpu_frame.hide()
            self.b_detail.setText("Show Details")

    def createProgressBarTotal(self, layout):
        self.total_progressBarLayout = QHBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        
        label = QLabel()
        label.setText("Total")

        #timer = QTimer(self)
        #timer.timeout.connect(self.totalCCPUProgressBarUpdate)
        #timer.start(1000)
        self.b_detail = QPushButton("ShowDetail")
        self.b_detail.setCheckable(True)
        self.b_detail.clicked.connect(self.show_detail_clicked)
        self.total_progressBarLayout.addWidget(label)
        self.total_progressBarLayout.addWidget(self.progressBar)
        self.total_progressBarLayout.addWidget(self.b_detail)
        layout.addLayout(self.total_progressBarLayout)


    def createProgressBarXCPU(self, layout):
        self.progressBarXcpu = []
        cpu_count = psutil.cpu_count()
        self.progressBar_x_cpu_frame = QFrame()
        self.progressBar_x_cpu_Layout = QVBoxLayout()
        for i in range (cpu_count):
            self.progressBarXcpu.append(QProgressBar())
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
        #layout.addLayout(self.progressBar_x_cpu_Layout)
        layout.addWidget(self.progressBar_x_cpu_frame)

        
        #timer = QTimer(self)
        #timer.timeout.connect(self.CPUProgressBarUpdateXCPU)
        #timer.start(1000)

    

    def createFrequencyHandler(self,layout):
        self.frequencyLabel = QLabel()
        self.frequencyLabel.setText("Set Frequency")
        self.applyFrequency = QPushButton()
        self.applyFrequency.setText("Apply")
        self.applyFrequency.setGeometry(0,0,100,50 )
        self.editFrequencyText = QLineEdit("1000")

        self.applyFrequency.clicked.connect(self.updateFrequency)
        
        self.frequencyLayout = QHBoxLayout()
        self.frequencyLayout.addWidget(self.frequencyLabel)
        self.frequencyLayout.addWidget(self.editFrequencyText)
        self.frequencyLayout.addWidget(self.applyFrequency)
        layout.addLayout(self.frequencyLayout)

    def updateFrequency(self):
        value_string = re.search(r'\d+\.\d+|\d+', self.editFrequencyText.toPlainText())
        if value_string is not None:
            new_frequency = float(value_string.group())
            self.setFrequency(new_frequency)
            self.setInterval(self.timer, new_frequency)


class DataGrabber(QObject):
    finished = pyqtSignal()

    results = pyqtSignal(dict)  # set the type of object you are sending

    def __init__(self):
        super().__init__()
        self.count = 0

    def calculateCPUUsageXCPU(self, cpu_interval):
        return psutil.cpu_percent(interval=cpu_interval, percpu=True)

    def run(self):
        while True:

            try:
                self.frequency = 1000
                self.value_total = 0.0
                self.value_x_cpu = self.calculateCPUUsageXCPU(self.frequency / 1000)
                self.cpu_count = psutil.cpu_count()
                for i in range (self.cpu_count):
                    self.value_total += self.value_x_cpu[i]
                self.value_total /= self.cpu_count
                print("pre-send-result")
                self.send_results()  # when done, send the results
            except:
                traceback.print_exc()

        self.finished.emit()

    def send_results(self):
        print("Send Result")
        results = {'value_total': self.value_total, 'value_x_cpu': self.value_x_cpu, 'cpu_count': self.cpu_count}
        self.results.emit(results)

