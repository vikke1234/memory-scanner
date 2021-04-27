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

import typing
from enum import IntEnum

import psutil
from PyQt5.Qt import QAbstractTableModel, QModelIndex, Qt


class HeaderEnum(IntEnum):
    PID = 0
    NAME = 1
    USER = 2
    PATH = 3


class ProcessViewModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
                except psutil.AccessDenied:
                    return ""
        return None
