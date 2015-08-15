from PySide.QtGui import QDialog
from ..gui.new_image_dialog import Ui_NewImageDialog


class NewImageDialog(QDialog):

    def __init__(self, parent=None):

        super(NewImageDialog, self).__init__(parent)
        self.ui = Ui_NewImageDialog()
        self.ui.setupUi(self)
        self.size = None

        self.ui.done_button.clicked.connect(self.done_clicked)

    def done_clicked(self):
        self.size = (self.ui.width_box.value(), self.ui.height_box.value())
        self.close()

    def get_size(self):
        return self.size
