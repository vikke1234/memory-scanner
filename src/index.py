from gui.MainWindow import MainWindow
from PyQt5.Qt import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
