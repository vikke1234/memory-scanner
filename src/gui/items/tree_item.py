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

from core.value import Value


class SavedAddressHeaderEnum(IntEnum):
    """
    Header indexes for the saved address model
    """
    DESCRIPTION = 0
    ADDRESS = auto()
    VALUE = auto()
    TYPE = auto()
    SIZE = auto()


class TreeItem:
    """
    This class is simply an internal data structure to manage the saved address tree

    if there will be more tree views which need items, this should probably be refactored
    to be an abstract class, for now though this will do. As it's fairly trivial to
    make this into an abstract one.
    """

    def __init__(self, data, parent=None):
        self._data: Value = data
        self.__parent: TreeItem = parent
        self.__children = []

    def append_child(self, item):
        """
        Appends a new child to a node

        :param item: item to append
        :return: None
        """
        self.__children.append(item)

    def child(self, row):
        """
        :param row: index of the child
        :return: returns the child of an item at a given index
        """
        if row < 0 or row >= len(self.__children):
            return None
        return self.__children[row]

    @property
    def children(self):
        return self.__children

    def child_count(self):
        """

        :return: returns the amount of children a node has
        """
        return len(self.__children)

    def row(self):
        """

        :return: returns the index of the current node in it's parent
        """
        if self.__parent:
            self.__parent.__children.index(self)
        return 0

    def data(self, column: int):
        """
        fetches data from the item
        :param column: column for the data
        :return: data contained in the cell
        """
        if column == SavedAddressHeaderEnum.ADDRESS:
            return hex(self._data.address)
        if column == SavedAddressHeaderEnum.VALUE:
            return self._data.value
        if column == SavedAddressHeaderEnum.TYPE:
            return self._data.type
        if column == SavedAddressHeaderEnum.DESCRIPTION:
            return ""
        return None

    def set_data(self, column: int, value):
        """
        Sets the data in a given column

        :param column: column to place it in
        :param value: data
        :return: True if success, else False
        """
        if self._data is None:
            return False

        if column == SavedAddressHeaderEnum.TYPE:
            self._data.change_type(value)
            return True
        if column == SavedAddressHeaderEnum.VALUE:
            pass  # this will be a little more complex, I'll figure this out later
        if column == SavedAddressHeaderEnum.DESCRIPTION:
            pass
        return False

    def insert_children(self, position: int, count: int):
        """
        inserts count amount of children into a node

        :param position: position to start
        :param count: amount to insert
        :return: True if it succeeded, otherwise false
        """
        if not 0 < position:
            return False

        for row in range(count):
            self.__children.insert(position, None)
        return True

    def remove_children(self, position: int, count: int):
        """
        removes count amount of children from the node

        :param position: position to start from
        :param count: amount to remove
        :return: True if succeeded, else false
        """
        if not 0 < position < self.child_count():
            return False

        del self.__children[position:count+1]
        return True

    @property
    def parent(self):
        """
        fetches the parent

        :return: The parent node
        """
        return self.__parent

    def get_internal_pointer(self):
        """
        fetches the raw content, in this case: a Value
        :return: the Value contained in the TreeItem
        """
        return self._data