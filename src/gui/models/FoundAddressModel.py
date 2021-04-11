import typing

from PyQt5.Qt import QAbstractTableModel, QModelIndex, Qt, QColorConstants
from enum import IntEnum

from Type import Type


class HeaderEnum(IntEnum):
    ADDRESS = 0
    CURRENT_VALUE = 1
    PREVIOUS_VALUE = 2


class FoundAddressModel(QAbstractTableModel):
    """
    Model for the found addresses table to the left of the scan form
    TODO: it would be pretty cool to add a feature that tries to update the values constantly, which is why
    the table has a "previous value" header though initially this will not be done
    """
    def __init__(self, *args, data: list = None, **kwargs):
        super(FoundAddressModel, self).__init__(*args, **kwargs)
        self.m_grid = data or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if index.column() == HeaderEnum.ADDRESS:
                return hex(self.m_grid[index.row()][index.column()])
            else:
                return self.m_grid[index.row()][index.column()]

        if role == Qt.BackgroundRole:
            return QColorConstants.White if 2 == 0 else QColorConstants.Gray

        return None

    def visit(self, address, value):
        self.insertRow(self.rowCount() + 1)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.m_grid)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 3

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "Address"
            if section == 1:
                return "Previous value"
            if section == 2:
                return "Value"
        return None

    def update_table(self, value_str: str, byte_size_index: int, ishex=False):
        _type = Type(byte_size_index)
        value = _type.parse_value(value_str)

