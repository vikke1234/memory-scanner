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
from PyQt5.QtCore import QModelIndex

from gui.items.tree_item import TreeItem, SavedAddressHeaderEnum
from memory.value import Value


class SavedAddressModel(QAbstractItemModel):
    """
    This model is for saving entries, it's a tree model so you can group them together
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._root_item = TreeItem(None)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            item: TreeItem = index.internalPointer()
            return item.data(index.column())

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
        if parent.column() > 0:
            return 0

        return self._root_item.childCount()

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_item = self._root_item

        if parent.isValid():
            parent_item = parent.internalPointer()

        child = parent_item.child(row)

        if child:
            return self.createIndex(row, column, child)
        return QModelIndex()

    def parent(self, child: QModelIndex) -> QModelIndex:
        if not child.isValid():
            return QModelIndex()
        parent_item: TreeItem = child.internalPointer().parent

        if parent_item == self._root_item:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return QAbstractItemModel.flags(self, index)

    def append_row(self, value: Value):
        self._root_item.appendChild(TreeItem(value, self._root_item))
        self.layoutChanged.emit()
