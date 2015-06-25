from PySide.QtGui import QDialog
from ..gui.brush_dialog import Ui_BrushDialog


class BrushDialog(QDialog):

    def __init__(self, parent=None):

        super(BrushDialog, self).__init__(parent)
        self.ui = Ui_BrushDialog()
        self.ui.setupUi(self)
