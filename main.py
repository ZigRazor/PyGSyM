
import sys
#from PySide6.QtWidgets import QApplication, QLabel
from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from qtpy.QtCore import Slot

import main_window2
import main_window

import os
import subprocess
import re
import shutil
import psutil

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    form = main_window.Main_Window()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())    