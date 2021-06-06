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
import math
import operator
import struct

from PyQt5.Qt import QMainWindow, QHeaderView, QMessageBox
from PyQt5.QtCore import pyqtSlot, QModelIndex, QLocale, QRegExp
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from psutil import NoSuchProcess

from gui.dialogs.process_view import ProcessView
from gui.dialogs.write_form import WriteForm
from gui.items.tree_item import TreeItem
from gui.models.found_address_model import FoundAddressModel
from gui.models.saved_address_model import SavedAddressHeaderEnum
from gui.ui.widgets.mainwindow import Ui_MainWindow
from core.memory import Memory
from core.type import Type


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.memory = Memory()

        self.setupUi(self)
        self.scan_byte_size.insertItems(0, [str(t) for t in Type])
        self.scan_byte_size.setCurrentIndex(Type.UINT32.value)
        self.scan_widget.setEnabled(False)

        self.found_table.setModel(FoundAddressModel(self))
        self.found_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.new_scan.clicked.connect(self.new_scan_clicked)
        self.next_scan.clicked.connect(self.next_scan_clicked)
        self.actionAttach.triggered.connect(self.attach_triggered)
        self.found_table.doubleClicked.connect(self.found_table_double_clicked)
        self.saved_results.doubleClicked.connect(self.saved_model_double_clicked)
        self.search_for.setValidator(QIntValidator(self))
        self.scan_byte_size.currentIndexChanged.connect(self.type_changed)

    @pyqtSlot(int)
    def type_changed(self, index):
        int_validator = QIntValidator(self)
        double_validator = QRegExpValidator(QRegExp(r"-?[0-9]*[\.\,]?[0-9]*"))
        type_to_validator = {Type.UINT8: int_validator, Type.UINT16: int_validator,
                             Type.UINT32: int_validator, Type.UINT64: int_validator,
                             Type.FLOAT: double_validator, Type.DOUBLE: double_validator}
        self.search_for.setValidator(type_to_validator[Type(index)])

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
        # TODO: fix looking for negative values, probably have to fiddle with the type system
        try:
            scan_type = {0: operator.eq, 1: operator.gt, 2: operator.lt, 3: operator.ne}
            match_index = self.scan_matching.currentIndex()
            type_ = Type(self.scan_byte_size.currentIndex())

            # since floating points are annoying we have to use isclose, I kinda wanna make
            # it configureable though but for now it will have to do
            if type_ == Type.FLOAT or type_ == Type.DOUBLE:
                scan_type[1] = math.isclose

            values = self.memory.scan(self.search_for.text(), type_, scan_type[match_index])
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

    @pyqtSlot(QModelIndex)
    def saved_model_double_clicked(self, index: QModelIndex):
        if not index.isValid():
            return
        column = index.column()

        if column == SavedAddressHeaderEnum.VALUE:
            form = WriteForm(self)
            x = form.exec_()
            text = form.value.text()
            if x and len(text) != 0:
                item: TreeItem = self.saved_results.model().get_item(index)
                value = item.get_internal_pointer()
                try:
                    value.write(value.type.parse_value(text, form.ishex.isChecked()))
                except struct.error:
                    QMessageBox(QMessageBox.NoIcon, "Error", "You can't write a larger number to "
                                                             "memory than you currently have set "
                                                             "as a type.\nSee limits.h for more "
                                                             "information",
                                QMessageBox.Ok, self).exec_()
                except ValueError:
                    # this is a kinda temporary fix, I'm planning on adding a validator or some
                    # shit later, not entirely sure how to add them yet so this will do
                    QMessageBox(QMessageBox.NoIcon, "Error", "Error parsing value, you probably "
                                                             "entered text when trying to write "
                                                             "an integer...",
                                QMessageBox.Ok, self).exec_()
