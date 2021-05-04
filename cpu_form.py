from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from qtpy.QtCore import QDateTime, Qt, QTimer, Slot
import psutil

import re


class Cpu_Form(QDialog):

    def __init__(self, parent=None):
        super(Cpu_Form, self).__init__(parent)
        # Create widgets
                
        # Create layout and add widgets
        layout = QVBoxLayout()        

        self.setFrequency(1000.0)   
        self.timer = QTimer(self)
                       
        self.createFrequencyHandler(layout)
        self.createProgressBarTotal(layout)
        self.createProgressBarXCPU(layout)

        self.timer.timeout.connect(self.updateCpuStat)
        self.timer.start(1000)
        self.setInterval(self.timer,self.frequency/1000)

        
        # Set dialog layout
        self.setLayout(layout)

    def setFrequency(self, new_frequency: float):
        self.frequency = new_frequency
    
    def setInterval(self, timer, newInterval):
        timer.setInterval(newInterval)

    def updateCpuStat(self):        
        value_total = 0.0
        value_x_cpu = self.calculateCPUUsageXCPU(self.frequency/1000)
        cpu_count = psutil.cpu_count()
            
        for i in range (cpu_count):
            value_total += value_x_cpu[i]
            self.setProgressBarValue(self.progressBarXcpu[i] ,value_x_cpu[i])
        value_total /= cpu_count
        self.setProgressBarValue(self.progressBar ,value_total)    

    def setProgressBarValue(self, progressBar : QProgressBar, value : float):
        progressBar.setValue(value)

    def calculateCPUUsageTotal(self, cpu_interval):
        return psutil.cpu_percent(interval=cpu_interval)

    def calculateCPUUsageXCPU(self, cpu_interval):
        return psutil.cpu_percent(interval=cpu_interval, percpu=True)

    def totalCCPUProgressBarUpdate(self):
        self.setProgressBarValue(self.progressBar ,self.calculateCPUUsageTotal(self.frequency/1000))

    def CPUProgressBarUpdateXCPU(self):
        x_cpu_usage = self.calculateCPUUsageXCPU(self.frequency/1000)
        cpu_count = psutil.cpu_count()
        for i in range (cpu_count):
            self.setProgressBarValue(self.progressBarXcpu[i] ,x_cpu_usage[i])
        

    def createProgressBarTotal(self, layout):
        newLayout = QHBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        
        label = QLabel()
        label.setText("Total")

        #timer = QTimer(self)
        #timer.timeout.connect(self.totalCCPUProgressBarUpdate)
        #timer.start(1000)
        newLayout.addWidget(label)
        newLayout.addWidget(self.progressBar)
        layout.addLayout(newLayout)
    
    def createProgressBarXCPU(self, layout):
        self.progressBarXcpu = []
        cpu_count = psutil.cpu_count()
        for i in range (cpu_count):
            newLayout = QHBoxLayout()
            self.progressBarXcpu.append(QProgressBar())
            self.progressBarXcpu[i].setRange(0, 100)
            self.progressBarXcpu[i].setValue(0)
            label = QLabel()
            label.setText("CPU " + str(i))
            newLayout.addWidget(label)
            newLayout.addWidget(self.progressBarXcpu[i])
            layout.addLayout(newLayout)
        
        #timer = QTimer(self)
        #timer.timeout.connect(self.CPUProgressBarUpdateXCPU)
        #timer.start(1000)

    

    def createFrequencyHandler(self,layout):
        self.frequencyLabel = QLabel()
        self.frequencyLabel.setText("Set Frequency")
        self.applyFrequency = QPushButton()
        self.applyFrequency.setText("Apply")
        self.editFrequencyText = QTextEdit("1000")

        self.applyFrequency.clicked.connect(self.updateFrequency)
        
        newLayout = QHBoxLayout()
        newLayout.addWidget(self.frequencyLabel)
        newLayout.addWidget(self.editFrequencyText)
        newLayout.addWidget(self.applyFrequency)
        layout.addLayout(newLayout)

    def updateFrequency(self):
        value_string = re.search(r'\d+\.\d+|\d+', self.editFrequencyText.toPlainText())
        if value_string is not None:
            new_frequency = float(value_string.group())
            self.setFrequency(new_frequency)
            self.setInterval(self.timer, new_frequency)
    