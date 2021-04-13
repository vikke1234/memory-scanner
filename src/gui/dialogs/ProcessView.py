from PyQt5.Qt import Qt, QDialog
from gui.ui.dialogs.processview import Ui_ProcessViewDialog
from gui.models.ProcessViewModel import ProcessViewModel

class ProcessView(QDialog, Ui_ProcessViewDialog):
    def __init__(self, parent=None):
        super(ProcessView, self).__init__(parent=parent)
        self.setupUi(self)
        self.process_table.setModel(ProcessViewModel())
        self.process_table.horizontalHeader().stretchLastSection()

        self.attach_button.clicked.connect(self.attach)
        self.cancel_button.clicked.connect(lambda: self.reject())

    def attach(self):
        selection_model = self.process_table.selectionModel()
        if not selection_model.hasSelection():
            return
        row = selection_model.selectedRows().pop()
        pid = self.process_table.model().index(row.row(), 0).data()
        self.done(pid)
