from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                            QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QProgressBar, QPushButton,
                            QRadioButton, QScrollBar, QSizePolicy,
                            QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                            QVBoxLayout, QWidget, QFrame, QLineEdit)
from qtpy.QtCore import QDateTime, Qt, QTimer, Slot, QThread, QObject, QRunnable, Signal
from qtpy.QtGui import QMouseEvent
import psutil


class CpuBaseFrame(QFrame):
    
    def __init__(self):
        super().__init__()
        # widget
        self.label_cpu_time_user = QLabel("user")
        self.label_cpu_time_system = QLabel("system")
        self.label_cpu_time_idle = QLabel("idle")
        self.label_cpu_time_interrupt = QLabel("interrupt")
        self.label_cpu_time_dpc = QLabel("dpc")
        self.label_value_cpu_time_user = QLabel("0.0")
        self.label_value_cpu_time_system = QLabel("0.0")
        self.label_value_cpu_time_idle = QLabel("0.0")
        self.label_value_cpu_time_interrupt = QLabel("0.0")
        self.label_value_cpu_time_dpc = QLabel("0.0")

        self.pb_cpu = QProgressBar()
        self.l_cpu = QLabel()
        
        # layout
        self.lay_cpu = QHBoxLayout()

        # initialize
        self.pb_cpu.setRange(0, 100)
        self.pb_cpu.setValue(0)

        self.lay_cpu.addWidget(self.l_cpu)
        self.lay_cpu.addWidget(self.pb_cpu)
        self.setLayout(self.lay_cpu)
        # self.layout.addWidget(self.progressBar_total_frame)

    def setLabelText(self, text: str):        
        self.l_cpu.setText(text)


    def switch_progress_bar_total(self):

        if self.pb_cpu.isHidden():
            for i in reversed(range(self.lay_cpu.count())):
                self.lay_cpu.itemAt(i).widget().hide()
                self.lay_cpu.itemAt(i).widget().setParent(None)
            self.lay_cpu.addWidget(self.l_cpu)
            self.lay_cpu.addWidget(self.pb_cpu)            
            for i in reversed(range(self.lay_cpu.count())):
                self.lay_cpu.itemAt(i).widget().show()

        else:
            for i in reversed(range(self.lay_cpu.count())):
                self.lay_cpu.itemAt(i).widget().hide()
                self.lay_cpu.itemAt(i).widget().setParent(None)
            self.lay_cpu.addWidget(self.l_cpu)
            self.lay_cpu.addWidget(self.label_cpu_time_user)
            self.lay_cpu.addWidget(self.label_value_cpu_time_user)
            self.lay_cpu.addWidget(self.label_cpu_time_system)
            self.lay_cpu.addWidget(self.label_value_cpu_time_system)
            self.lay_cpu.addWidget(self.label_cpu_time_idle)
            self.lay_cpu.addWidget(self.label_value_cpu_time_idle)
            self.lay_cpu.addWidget(self.label_cpu_time_interrupt)
            self.lay_cpu.addWidget(self.label_value_cpu_time_interrupt)
            self.lay_cpu.addWidget(self.label_cpu_time_dpc)
            self.lay_cpu.addWidget(self.label_value_cpu_time_dpc)
            for i in reversed(range(self.lay_cpu.count())):
                self.lay_cpu.itemAt(i).widget().show()

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        self.switch_progress_bar_total()
   
    def update_cpu_percent_stat(self, values):
        self.pb_cpu.setValue(values)

    def update_cpu_times_stat(self, values):
        self.label_value_cpu_time_user.setText("{:3.2f}".format(values["user"]))
        self.label_value_cpu_time_system.setText("{:3.2f}".format(values["system"]))
        self.label_value_cpu_time_idle.setText("{:3.2f}".format(values["idle"]))
        self.label_value_cpu_time_interrupt.setText("{:3.2f}".format(values["interrupt"]))
        self.label_value_cpu_time_dpc.setText("{:3.2f}".format(values["dpc"]))



class CpuTotalFrame(QFrame):
    show_detail = Signal(bool)

    def __init__(self):
        super().__init__()
        # widget
        
        self.f_total_cpu = CpuBaseFrame()
        self.b_detail = QPushButton("ShowDetail")

        # layout
        self.lay_total_cpu = QHBoxLayout()

        # initialize
        self.f_total_cpu.setLabelText("Total")
        self.b_detail.setCheckable(True)
        self.b_detail.clicked.connect(self.show_detail_clicked)
        self.lay_total_cpu.addWidget(self.f_total_cpu)
        self.lay_total_cpu.addWidget(self.b_detail)
        self.setLayout(self.lay_total_cpu)

    def show_detail_clicked(self):
        if self.b_detail.isChecked():
            self.show_detail.emit(True)
            self.b_detail.setText("Hide Details")
        else:
            self.show_detail.emit(False)
            self.b_detail.setText("Show Details")

    def update_cpu_percent_stat(self, stats):        
        value_total = stats['value_total']
        self.f_total_cpu.update_cpu_percent_stat(value_total)

    def update_cpu_times_stat(self, stats):
        value_total = stats['value_total']
        self.f_total_cpu.update_cpu_times_stat(value_total)


class CpuDetailedFrame(QFrame):
    show_detail = Signal(bool)

    def __init__(self):
        super().__init__()
        # widget
                
        self.f_detailed_cpu = [] 
        self.l_detailed_cpu = [] 

        # layout
        self.lay_detailed_cpu = QVBoxLayout()
        self.sub_f_detailed_cpu = [] 
        self.sub_lay_detailed_cpu = [] 

        # initialize
        self.cpu_count = psutil.cpu_count()
        for i in range (self.cpu_count):            
            self.f_detailed_cpu.append(CpuBaseFrame())
            self.f_detailed_cpu[i].setLabelText("CPU " + str(i))
            self.lay_detailed_cpu.addWidget(self.f_detailed_cpu[i])
            
                
        self.setLayout(self.lay_detailed_cpu)

    def update_cpu_percent_stat(self, stats):
        value_x_cpu = stats['value_x_cpu']
        for i in range (self.cpu_count):            
            self.f_detailed_cpu[i].update_cpu_percent_stat(value_x_cpu[i])

    def update_cpu_times_stat(self, stats):
        value_x_cpu = stats['value_x_cpu']
        for i in range (self.cpu_count):  
            self.f_detailed_cpu[i].update_cpu_times_stat(value_x_cpu[i])
            
