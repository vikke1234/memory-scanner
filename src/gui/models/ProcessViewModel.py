from PyQt5.Qt import QAbstractTableModel, QModelIndex, Qt
from enum import IntEnum
import psutil
import typing


class HeaderEnum(IntEnum):
    PID = 0
    NAME = 1
    USER = 2
    PATH = 3


class ProcessViewModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(ProcessViewModel, self).__init__(*args, **kwargs)
        self.processes = list(psutil.process_iter())

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.processes)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 4

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == HeaderEnum.PID:
                return "PID"
            if section == HeaderEnum.NAME:
                return "Name"
            if section == HeaderEnum.USER:
                return "USER"
            if section == HeaderEnum.PATH:
                return "Path"
        return None

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if index.column() == HeaderEnum.PID:
                return self.processes[index.row()].pid
            if index.column() == HeaderEnum.NAME:
                return self.processes[index.row()].name()
            if index.column() == HeaderEnum.USER:
                return self.processes[index.row()].username()
            if index.column() == HeaderEnum.PATH:
                try:
                    return self.processes[index.row()].exe()
                except psutil.AccessDenied as e:
                    return ""
