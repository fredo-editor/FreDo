from PySide.QtGui import QDialog
from ..gui.about_dialog import Ui_AboutDialog


class AboutDialog(QDialog):

    def __init__(self, parent=None):

        super(AboutDialog, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
