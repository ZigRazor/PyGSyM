from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from qtpy.QtCore import QDateTime, Qt, QTimer, Slot

import cpu_form

class Main_Window(QDialog):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTabWidget()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        
        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)        
        mainLayout.addWidget(self.TabWidget, 1, 0, 2, 2)
        mainLayout.setRowStretch(1, 2)
        #mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 2)
        #mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")
        self.changeStyle('Fusion')


    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def createTabWidget(self):
        self.TabWidget = QTabWidget()
        self.TabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        #tableWidget = QTableWidget(10, 10)
        cpu_form1 = cpu_form.Cpu_Form()
        tab1hbox = QHBoxLayout()
        #tab1hbox.setContentsMargins(5, 5, 5, 5)
        #tab1hbox.addWidget(tableWidget)
        tab1hbox.addWidget(cpu_form1)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.TabWidget.addTab(tab1, "&CPU")
        self.TabWidget.addTab(tab2, "Text &Edit")
