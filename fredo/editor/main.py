from ..gui.main_window import Ui_EditorMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui
import sys


class EditorMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(EditorMainWindow, self).__init__(parent)
        self.ui = Ui_EditorMainWindow()
        self.ui.setupUi(self)
        self.ui.action_open.triggered.connect(self.open_file)

    def open_file(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")[0]
        if file_name:
            image = QtGui.QImage(file_name)
            for x in dir(image):
                print(x)
            if image.isNull():
                QtWidgets.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % file_name)
                return
            self.ui.image_label.setPixmap(QtGui.QPixmap.fromImage(image))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    calculator = EditorMainWindow()
    calculator.show()
    sys.exit(app.exec_())
