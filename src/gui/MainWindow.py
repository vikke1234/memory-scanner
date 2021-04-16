from PyQt5.QtWidgets import QDialog

from Memory import Memory
from Type import Type
from gui.models.ProcessViewModel import ProcessViewModel
from gui.ui.widgets.mainwindow import Ui_MainWindow
from PyQt5.Qt import QMainWindow, QHeaderView
from gui.models.FoundAddressModel import FoundAddressModel
from gui.dialogs.ProcessView import ProcessView
from PyQt5.Qt import QDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.memory = Memory()

        self.setupUi(self)
        self.scan_widget.setEnabled(False)

        self.found_table.setModel(FoundAddressModel())

        self.found_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.new_scan.clicked.connect(self.new_scan_clicked)
        self.actionAttach.triggered.connect(self.attach_triggered)

    def new_scan_clicked(self):
        values = self.memory.scan(123, Type(self.scan_byte_size.currentIndex()), aligned=self.aligned.isChecked())
        self.found_table.model().setValues(values)

    def next_scan_clicked(self):
        pass

    def attach_triggered(self):
        process_view = ProcessView()
        pid = process_view.exec_()
        if pid != 0:
            self.memory.attach(pid)
            self.scan_widget.setEnabled(True)