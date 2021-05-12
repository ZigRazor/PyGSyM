import sys
from qtpy.QtWidgets import QApplication

import mainwindow

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    app.processEvents()

    form = mainwindow.MainWindow()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
