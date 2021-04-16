import typing
from typing import List
from enum import IntEnum

from PyQt5.Qt import QAbstractTableModel, QModelIndex, Qt, QColorConstants

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

    def __init__(self, *args, data: list = None, **kwargs):
        super(FoundAddressModel, self).__init__(*args, **kwargs)
        self.values: List[Value] = data or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if index.column() == HeaderEnum.ADDRESS:
                return hex(self.values[index.row()].address)
            if index.column() == HeaderEnum.PREVIOUS_VALUE:
                return self.values[index.row()].value
            if index.column() == HeaderEnum.CURRENT_VALUE:
                return None  # todo

        if role == Qt.BackgroundRole:
            return QColorConstants.White if 2 == 0 else QColorConstants.Gray

        return None

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row+count)
        for _ in range(count):
            self.values.append(None)
        self.endInsertRows()

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
        self.insertRows(0, len(values), self)
        self.values = values
