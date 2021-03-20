from src.gui.MainWindow import MainWindow
from PyQt5 import Qt

if __name__ == '__main__':
    import sys
    app = Qt.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
