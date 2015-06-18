from ..gui.main_window import Ui_EditorMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class EditorMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(EditorMainWindow, self).__init__(parent)
        self.ui = Ui_EditorMainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    calculator = EditorMainWindow()
    calculator.show()
    sys.exit(app.exec_())
