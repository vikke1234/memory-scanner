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

from PyQt5.Qt import QDialog

from gui.models.process_view_model import ProcessViewModel
from gui.ui.dialogs.processview import Ui_ProcessViewDialog


class ProcessView(QDialog, Ui_ProcessViewDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.process_table.setModel(ProcessViewModel())
        self.process_table.horizontalHeader().stretchLastSection()

        self.process_table.doubleClicked.connect(self.attach)
        self.attach_button.clicked.connect(self.attach)
        self.cancel_button.clicked.connect(self.reject)

    def attach(self):
        selection_model = self.process_table.selectionModel()
        if not selection_model.hasSelection():
            return
        row = selection_model.selectedRows().pop()
        pid = self.process_table.model().index(row.row(), 0).data()
        self.done(pid)
