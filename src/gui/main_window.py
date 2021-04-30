#      This file is part of ot-project.
#
#      ot-project is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      ot-project is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#

from PyQt5 import QtGui
from PyQt5.Qt import QMainWindow, QHeaderView
from PyQt5.QtCore import pyqtSlot

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

        self.found_table.setModel(FoundAddressModel(self))

        self.found_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.new_scan.clicked.connect(self.new_scan_clicked)
        self.next_scan.clicked.connect(self.next_scan_clicked)
        self.actionAttach.triggered.connect(self.attach_triggered)

    @pyqtSlot()
    def new_scan_clicked(self):
        if self.next_scan.isEnabled():
            self.next_scan.setEnabled(False)
            self.found_table.model().set_values([])
            self.memory.reset_scan()
        else:
            self.next_scan_clicked()
            self.next_scan.setEnabled(True)

    @pyqtSlot()
    def next_scan_clicked(self):
        values = self.memory.scan(self.search_for.text(), Type(
            self.scan_byte_size.currentIndex()), aligned=self.aligned.isChecked())
        self.amount_found.setText("Found: {}".format(len(values)))
        self.found_table.model().set_values(values)

    @pyqtSlot()
    def attach_triggered(self):
        process_view = ProcessView()
        pid = process_view.exec_()
        if pid != 0:
            self.memory.attach(pid)
            self.scan_widget.setEnabled(True)
