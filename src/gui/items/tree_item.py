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
from enum import IntEnum, auto

from value import Value


class SavedAddressHeaderEnum(IntEnum):
    """
    Header indexes for the saved address model
    """
    DESCRIPTION = auto()
    ADDRESS = auto()
    VALUE = auto()
    TYPE = auto()
    SIZE = auto()


class TreeItem:
    """
    This class is simply an internal datastructure to manage the tree
    """

    def __init__(self, data, parent=None):
        self._data: Value = data
        self._parent: TreeItem = parent
        self._children = []

    def appendChild(self, item):
        self._children.append(item)
        self._parent = self

    def child(self, row):
        if row < 0 or row >= len(self._children):
            return None
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def row(self):
        if self._parent:
            self._parent._children.index(self)
        return 0

    def data(self, column):
        if column == SavedAddressHeaderEnum.ADDRESS:
            return hex(self._data.address)
        if column == SavedAddressHeaderEnum.VALUE:
            return self._data.value
        if column == SavedAddressHeaderEnum.TYPE:
            return self._data.type.name.lower()
        if column == SavedAddressHeaderEnum.DESCRIPTION:
            return ""

    @property
    def parent(self):
        return self._parent
