from ..gui.main_window import Ui_EditorMainWindow
from PyQt4.QtGui import QApplication, QMainWindow
from PyQt4 import QtGui
import sys


class EditorMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(EditorMainWindow, self).__init__(parent)
        self.ui = Ui_EditorMainWindow()
        self.ui.setupUi(self)
        self.ui.action_open.triggered.connect(self.open_file)

    def open_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open File")
        if file_name:
            image = QtGui.QImage(file_name)

            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                                              "Cannot load %s." % file_name)
                return
            self.ui.image_label.setPixmap(QtGui.QPixmap.fromImage(image))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    calculator = EditorMainWindow()
    calculator.show()
    sys.exit(app.exec_())
