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
            self.lay_total_cpu.removeWidget(self.pb_total_cpu)
            self.lay_total_cpu.removeWidget(self.b_detail)
            self.pb_total_cpu.hide()
            self.b_detail.hide()

            self.lay_total_cpu.addWidget(self.label_cpu_time_user)
            self.lay_total_cpu.addWidget(self.label_value_cpu_time_user)
            self.lay_total_cpu.addWidget(self.label_cpu_time_system)
            self.lay_total_cpu.addWidget(self.label_value_cpu_time_system)
            self.lay_total_cpu.addWidget(self.label_cpu_time_idle)
            self.lay_total_cpu.addWidget(self.label_value_cpu_time_idle)
            self.lay_total_cpu.addWidget(self.label_cpu_time_interrupt)
            self.lay_total_cpu.addWidget(self.label_value_cpu_time_interrupt)
            self.lay_total_cpu.addWidget(self.label_cpu_time_dpc)
            self.lay_total_cpu.addWidget(self.label_value_cpu_time_dpc)
            self.lay_total_cpu.addWidget(self.b_detail)
            for i in reversed(range(self.lay_total_cpu.count())):                 
                self.lay_total_cpu.itemAt(i).widget().show()  
            #self.label_test.hide()
            #self.button_test.hide()
            #self.pb_total_cpu.show()
            #self.b_detail.show()
        else: 
            for i in reversed(range(self.lay_total_cpu.count())):                 
                self.lay_total_cpu.itemAt(i).widget().hide()           
            self.lay_total_cpu.removeWidget(self.label_cpu_time_user)
            self.lay_total_cpu.removeWidget(self.label_value_cpu_time_user)
            self.lay_total_cpu.removeWidget(self.label_cpu_time_system)
            self.lay_total_cpu.removeWidget(self.label_value_cpu_time_system)
            self.lay_total_cpu.removeWidget(self.label_cpu_time_idle)
            self.lay_total_cpu.removeWidget(self.label_value_cpu_time_idle)
            self.lay_total_cpu.removeWidget(self.label_cpu_time_interrupt)
            self.lay_total_cpu.removeWidget(self.label_value_cpu_time_interrupt)
            self.lay_total_cpu.removeWidget(self.label_cpu_time_dpc)
            self.lay_total_cpu.removeWidget(self.label_value_cpu_time_dpc)
            self.lay_total_cpu.removeWidget(self.b_detail)
            self.lay_total_cpu.addWidget(self.pb_total_cpu)
            self.lay_total_cpu.addWidget(self.b_detail)
            for i in reversed(range(self.lay_total_cpu.count())):                 
                self.lay_total_cpu.itemAt(i).widget().show()  
            #self.label_test.show()
            #self.button_test.show()
            #self.pb_total_cpu.hide()
            #self.b_detail.hide()

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

    def update_cpu_percent_stat(self, stats):
        value_total = stats['value_total']
        self.pb_total_cpu.setValue(value_total)

    def update_cpu_times_stat(self, stats):
        value_total = stats['value_total']
        self.label_value_cpu_time_user = QLabel(str(value_total["user"]))
        self.label_value_cpu_time_system = QLabel(str(value_total["system"]))
        self.label_value_cpu_time_idle = QLabel(str(value_total["idle"]))
        self.label_value_cpu_time_interrupt = QLabel(str(value_total["interrupt"]))
        self.label_value_cpu_time_dpc = QLabel(str(value_total["dpc"]))
