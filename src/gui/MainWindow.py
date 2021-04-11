from gui.ui.mainwindow import Ui_MainWindow
from PyQt5.Qt import QMainWindow, QHeaderView
from gui.models.FoundAddressModel import FoundAddressModel

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.found_table.setModel(FoundAddressModel())
        self.found_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.new_scan.clicked.connect(self.new_scan_clicked)
        self.new_scan.setEnabled(True)

    def new_scan_clicked(self):
        self.found_table.update_table(self.search_for.text(), self.search_byte_size.currentIndex())

    def next_scan_clicked(self):
        pass