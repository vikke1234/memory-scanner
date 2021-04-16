import sys

from PyQt5.Qt import QApplication

from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
