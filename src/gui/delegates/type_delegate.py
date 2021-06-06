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
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt, QStyledItemDelegate, QComboBox
from PyQt5.QtCore import pyqtSignal, QModelIndex
from PyQt5.QtWidgets import QWidget, QStyleOptionViewItem

from core.type import Type


class TypeDelegate(QStyledItemDelegate):
    """
    This is a delegate to allow changing of types in the saved address view
    """
    # combobox index, row
    type_changed_signal = pyqtSignal(int, QModelIndex)

    def __init__(self, parent=None):
        super().__init__(parent)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        editor.blockSignals(True)
        data = int(index.model().data(index))
        editor.setCurrentIndex(data)
        editor.blockSignals(False)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem,
                     index: QModelIndex) -> QWidget:
        combobox = QComboBox(parent)
        li = [str(t) for t in Type]
        combobox.addItems(li)
        combobox.setCurrentIndex(index.model().data(index))

        # There's probably a better way to do this, but since I don't know it, I'll make a new
        # signal for it, so I can get the row for the type. Time is limited, deadline is tomorrow
        combobox.currentIndexChanged.connect(lambda x:
                                             self.type_changed_signal.emit(x, index))
        return combobox

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel,
                     index: QtCore.QModelIndex) -> None:
        model.setData(index, editor.currentIndex())
