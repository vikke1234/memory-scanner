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
from queue import Queue
from time import sleep

from PyQt5.QtCore import QThread, QMutex, QMutexLocker, pyqtSignal

from gui.items.tree_item import TreeItem
from memory.value import Value

mutex = QMutex()


class SavedResultsThread(QThread):
    updated = pyqtSignal(TreeItem)

    def __init__(self, data: TreeItem, parent=None):
        super().__init__(parent)
        self.data = data
        self.running = True

    def run(self) -> None:
        stack = [self.data]

        while self.running:
            if len(stack) == 0:
                stack.append(self.data)
            while len(stack) > 0:
                with QMutexLocker(mutex):
                    item = stack.pop()
                    stack.extend(item.children)
                    value: Value = item.get_internal_pointer()
                    if value is None:
                        continue
                    previous = value.value

                    value.read()
                    if value != previous:
                        self.updated.emit(item)

            sleep(0.01)
    def stop(self):
        self.running = False
