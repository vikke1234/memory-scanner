import typing
from enum import IntEnum
from typing import List

from PyQt5.Qt import \
    QAbstractTableModel, \
    QModelIndex, \
    Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from gui.threads.update_scanresult import UpdateThread
from value import Value


class HeaderEnum(IntEnum):
    ADDRESS = 0
    CURRENT_VALUE = 1
    PREVIOUS_VALUE = 2


class FoundAddressModel(QAbstractTableModel):
    """
    Model for the found addresses table to the left of the scan form
    TODO: it would be pretty cool to add a feature that tries to update the values constantly, which
    is why the table has a "previous value" header though initially this will not be done
    """
    table_changed_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.values: List[Value] = []
        # this will update the "current value" column
        self.current_value_update_thread = UpdateThread([], parent=self)

        # this indicates when the entire table is set, so it knows when to start a new thread
        self.current_value_update_thread.changed_value.connect(self.current_value_changed)
        self.table_changed_signal.connect(self.table_changed)

        """
        NOTE: THIS LAMBDA IS INTENTIONAL, IT WILL NOT WORK IF YOU REMOVE THE LAMBDA AND WILL NOT
        WORK. https://machinekoder.com/how-to-not-shoot-yourself-in-the-foot-using-python-qt/
        """
        self.destroyed.connect(lambda: self.__unregister())

    def __unregister(self):
        """
        a makeshift destructor, since __del__ can't be relied on to be called on exit
        since the GC does whatever it wants.
        :return: None
        """
        self.current_value_update_thread.stop()
        self.current_value_update_thread.wait()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return None
        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            if column == HeaderEnum.ADDRESS:
                return hex(self.values[row].address)
            if column == HeaderEnum.CURRENT_VALUE:
                return self.values[row].value
            if column == HeaderEnum.PREVIOUS_VALUE:
                return self.values[row].previous_value
        return None

    def setData(self, index: QModelIndex, value: typing.Any, role: int = Qt.EditRole) -> bool:
        if not index.isValid():
            return False

        if role == Qt.EditRole:
            row = index.row()
            if index.column() == HeaderEnum.CURRENT_VALUE:
                self.values[row].value = value
            elif index.column() == HeaderEnum.PREVIOUS_VALUE:
                self.values[row].previous_value = value
            elif index.column() == HeaderEnum.ADDRESS:
                self.values[row].address = value

            self.dataChanged.emit(index, index, role)
            return True

        return False

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(parent, row, row + count)
        for _ in range(count):
            self.values.append(None)
        self.endInsertRows()

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        del self.values[row:row + count]
        self.endRemoveRows()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.values)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 3

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == HeaderEnum.ADDRESS:
                return "Address"
            if section == HeaderEnum.PREVIOUS_VALUE:
                return "Previous value"
            if section == HeaderEnum.CURRENT_VALUE:
                return "Value"
        return None

    def set_values(self, values: List[Value]):
        # pointless to show more than 100_000 addresses, the user won't be able
        # to sort through them anyway by hand
        if len(values) > self.rowCount():
            self.insertRows(0, min(len(values), 100_000), QModelIndex())
        else:
            self.removeRows(self.rowCount() - len(values), len(values), QModelIndex())

        self.values = values
        top_left = self.index(0, 0, QModelIndex())
        bottom_right = self.index(len(values), self.columnCount(), QModelIndex())

        self.dataChanged.emit(top_left, bottom_right)
        self.table_changed_signal.emit()

    @pyqtSlot(int)
    def current_value_changed(self, row):
        """
        slot to update a given rows value
        :param row: row of the value
        :return: None
        """
        value = self.values[row]
        index = self.index(row, HeaderEnum.CURRENT_VALUE, QModelIndex())
        self.setData(index, value.value)

    @pyqtSlot()
    def table_changed(self):
        """
        Simply starts the current value update thread if there's any values in the thread
        :return:
        """
        self.current_value_update_thread.stop()

        if len(self.values) > 0:
            self.current_value_update_thread = UpdateThread(self.values, self)
            self.current_value_update_thread.start()
