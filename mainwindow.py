from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                            QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                            QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                            QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                            QVBoxLayout, QWidget)
from qtpy.QtCore import QDateTime, Qt, QTimer, Slot

import CpuForm


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.TabWidget = QTabWidget()
        self.originalPalette = QApplication.palette()

        style_combo_box = QComboBox()
        style_combo_box.addItems(QStyleFactory.keys())

        style_label = QLabel("&Style:")
        style_label.setBuddy(style_combo_box)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disable_widgets_check_box = QCheckBox("&Disable widgets")

        self.create_tab_widget()

        style_combo_box.activated[str].connect(self.change_style)
        self.useStylePaletteCheckBox.toggled.connect(self.change_palette)

        top_layout = QHBoxLayout()
        top_layout.addWidget(style_label)
        top_layout.addWidget(style_combo_box)
        top_layout.addStretch(1)
        top_layout.addWidget(self.useStylePaletteCheckBox)

        main_layout = QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 2)
        main_layout.addWidget(self.TabWidget, 1, 0, 2, 2)
        main_layout.setRowStretch(1, 2)
        # main_layout.setRowStretch(2, 1)
        main_layout.setColumnStretch(0, 2)
        # main_layout.setColumnStretch(1, 1)
        self.setLayout(main_layout)

        self.setWindowTitle("PyGSyM")
        self.setAcceptDrops(True)
        self.setMinimumSize(600, 500)
        self.change_style('Fusion')

    def change_style(self, style_name):
        QApplication.setStyle(QStyleFactory.create(style_name))
        self.change_palette()

    def change_palette(self):
        if self.useStylePaletteCheckBox.isChecked():
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def create_tab_widget(self):
        self.TabWidget.setSizePolicy(QSizePolicy.Preferred,
                                     QSizePolicy.Ignored)

        tab1 = QWidget()
        # tableWidget = QTableWidget(10, 10)
        cpu_form1 = CpuForm.CpuForm()
        tab1hbox = QHBoxLayout()
        # tab1hbox.setContentsMargins(5, 5, 5, 5)
        # tab1hbox.addWidget(tableWidget)
        tab1hbox.addWidget(cpu_form1)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        text_edit = QTextEdit()

        text_edit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n"
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n"
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(text_edit)
        tab2.setLayout(tab2hbox)

        self.TabWidget.addTab(tab1, "&CPU")
        self.TabWidget.addTab(tab2, "Text &Edit")
