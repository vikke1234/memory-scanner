from PyQt5.Qt import QMainWindow, QHeaderView

from memory import Memory
from type import Type
from gui.dialogs.process_view import ProcessView
from gui.models.found_address_model import FoundAddressModel
from gui.ui.widgets.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.memory = Memory()

        self.setupUi(self)
        self.scan_widget.setEnabled(False)

        self.found_table.setModel(FoundAddressModel())

        self.found_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.new_scan.clicked.connect(self.new_scan_clicked)
        self.next_scan.clicked.connect(self.next_scan_clicked)
        self.actionAttach.triggered.connect(self.attach_triggered)

    def new_scan_clicked(self):
        if self.next_scan.isEnabled():
            self.next_scan.setEnabled(False)
            self.found_table.model().set_values([])
            self.memory.reset_scan()
        else:
            self.next_scan_clicked()
            self.next_scan.setEnabled(True)

    def next_scan_clicked(self):
        values = self.memory.scan(self.search_for.text(), Type(
            self.scan_byte_size.currentIndex()), aligned=self.aligned.isChecked())
        self.found_table.model().set_values(values)

    def attach_triggered(self):
        process_view = ProcessView()
        pid = process_view.exec_()
        if pid != 0:
            self.memory.attach(pid)
            self.scan_widget.setEnabled(True)
