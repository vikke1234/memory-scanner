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

from typing import List
from time import sleep

from PyQt5.Qt import QThread, QMutex
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QVariant

from value import Value


class UpdateThread(QThread):
    changed_value = pyqtSignal(int)

    def __init__(self, values, parent=None):
        super().__init__(parent)
        self.values: List[Value] = values
        self.__is_running: bool = True

    def run(self) -> None:
        while self.__is_running:
            for row, value in enumerate(self.values):
                current = value.read()
                if current != value.previous_value:
                    self.changed_value.emit(row)

                # not entirely sure about this
                if not self.__is_running:
                    break
            sleep(0.1)  # TODO: add a setting for this, for now it will stay static

    def stop(self):
        self.__is_running = False
