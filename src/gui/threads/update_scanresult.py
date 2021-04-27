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
