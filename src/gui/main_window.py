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

from PyQt5.Qt import QMainWindow, QHeaderView, QMessageBox
from PyQt5.QtCore import pyqtSlot, QModelIndex
from psutil import NoSuchProcess

from gui.dialogs.process_view import ProcessView
from gui.models.found_address_model import FoundAddressModel
from gui.models.saved_address_model import SavedAddressModel
from gui.ui.widgets.mainwindow import Ui_MainWindow
from memory.memory import Memory
from memory.type import Type


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
        self.found_table.doubleClicked.connect(self.found_table_double_clicked)

    @pyqtSlot()
    def new_scan_clicked(self):
        if self.next_scan.isEnabled():
            self.next_scan.setEnabled(False)
            self.found_table.model().set_values([])
            self.memory.reset_scan()
        else:
            # the isnumeric is a simple workaround, since I'll support strings eventually
            # until then it can stay
            if len(self.search_for.text()) > 0 and self.search_for.text().lstrip("-").isnumeric():
                self.next_scan_clicked()
                self.next_scan.setEnabled(True)

    @pyqtSlot()
    def next_scan_clicked(self):
        # TODO: fix looking for negative values, probably have to fiddle with the type system
        try:
            values = self.memory.scan(self.search_for.text(), Type(
                self.scan_byte_size.currentIndex()))
            self.amount_found.setText("Found: {}".format(len(values)))
            self.found_table.model().set_values(values)
        except NoSuchProcess:
            QMessageBox(QMessageBox.NoIcon, "Error", "No readable memory", QMessageBox.Ok,
                        self).exec_()

    @pyqtSlot()
    def attach_triggered(self):
        process_view = ProcessView()
        pid = process_view.exec_()
        if pid != 0:
            self.memory.attach(pid)
            self.scan_widget.setEnabled(True)

    @pyqtSlot(QModelIndex)
    def found_table_double_clicked(self, index: QModelIndex):
        if not index.isValid():
            return
        clicked_value = self.found_table.model().get_value(index.row())
        self.saved_results.model().append_row(clicked_value)
