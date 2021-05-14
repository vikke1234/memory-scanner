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

from PyQt5.Qt import QTreeView
from PyQt5.QtCore import QModelIndex, pyqtSlot

from gui.delegates.type_delegate import TypeDelegate
from gui.items.tree_item import SavedAddressHeaderEnum, TreeItem
from gui.models.saved_address_model import SavedAddressModel
from memory.type import Type


class SavedAddressView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._datamodel = SavedAddressModel(self)
        self.setModel(self._datamodel)
        type_delegate = TypeDelegate(self)
        type_delegate.type_changed_signal.connect(self.__change_data)
        self.setItemDelegateForColumn(SavedAddressHeaderEnum.TYPE, type_delegate)
        self._datamodel.layoutChanged.connect(self.__init_comboboxes)

    def append_row(self, value):
        """
        Places a value at the end of the root item

        :param value: Value to place
        :return: None
        """
        self._datamodel.append_row(value)

    def __init_comboboxes(self):
        """
        makes the comboboxes permanently show
        :return: None
        """
        for row in range(self._datamodel.rowCount(QModelIndex())):
            # Currently the sizes of the combo boxes are kinda fucked but I'll try to figure
            # that out at a later date.
            self.openPersistentEditor(self._datamodel.index(row, SavedAddressHeaderEnum.TYPE,
                                                            QModelIndex()))

    @pyqtSlot(int, QModelIndex)
    def __change_data(self, box_index, index):
        """
        slot for commitdata, it will swap the type currently in use

        :type box_index: index of the combobox
        :type index: index in the treeview
        :return: None
        """
        item: TreeItem = self._datamodel.get_item(index)
        item.set_data(SavedAddressHeaderEnum.TYPE, Type(box_index))
