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

from PyQt5.Qt import QAbstractItemModel, Qt
from PyQt5.QtCore import QModelIndex, QMutexLocker

from gui.items.tree_item import TreeItem, SavedAddressHeaderEnum
from gui.threads.saved_results_thread import SavedResultsThread, mutex
from memory.value import Value


class SavedAddressModel(QAbstractItemModel):
    """
    This model is for saving entries, it's a tree model so you can group them together
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._root_item = TreeItem(None)
        self.update_thread = SavedResultsThread(self._root_item, self)
        self.update_thread.updated.connect(self.value_changed)
        self.update_thread.start()
        self.destroyed.connect(lambda: self.__unregister())  # again, this is intentional.

    def __unregister(self):
        self.update_thread.stop()
        self.update_thread.wait()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            item: TreeItem = index.internalPointer()
            column = index.column()
            return item.data(column)

    def setData(self, index: QModelIndex, value: typing.Any, role: int = Qt.EditRole) -> bool:
        if not index.isValid():
            return False
        item: TreeItem = index.internalPointer()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == SavedAddressHeaderEnum.DESCRIPTION:
                    return "Description"
                if section == SavedAddressHeaderEnum.ADDRESS:
                    return "Address"
                if section == SavedAddressHeaderEnum.VALUE:
                    return "Value"
                if section == SavedAddressHeaderEnum.TYPE:
                    return "Type"

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return SavedAddressHeaderEnum.SIZE

    def rowCount(self, parent: QModelIndex = ...) -> int:
        parent_item = self.get_item(parent)
        if parent_item is None:
            return 0
        return self._root_item.child_count()

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_item = self.get_item(parent)
        if parent_item is None:
            return QModelIndex()

        child = parent_item.child(row)

        if child:
            return self.createIndex(row, column, child)
        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_item = self.get_item(index)
        parent_item: TreeItem = child_item.parent if child_item else None

        if parent_item == self._root_item or parent_item is None:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return QAbstractItemModel.flags(self, index)

    def append_row(self, value: Value):
        with QMutexLocker(mutex):
            self._root_item.append_child(TreeItem(value, self._root_item))
            self.layoutChanged.emit()

    def get_item(self, index: QModelIndex) -> TreeItem:
        if index.isValid():
            return index.internalPointer()
        return self._root_item

    def value_changed(self, item: TreeItem):
        index = self.createIndex(item.row(), SavedAddressHeaderEnum.VALUE, item.parent)
        self.dataChanged.emit(index, index)
