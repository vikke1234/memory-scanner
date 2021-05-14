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

from gui.ui.dialogs.write_form import Ui_WriteForm


class WriteForm(QDialog, Ui_WriteForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
