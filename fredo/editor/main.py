from ..gui.main_window import Ui_EditorMainWindow
from PyQt4.QtGui import QApplication, QMainWindow, QPixmap
from PyQt4 import QtGui
import sys
from .. import util


class EditorMainWindow(QMainWindow):

    def __init__(self, parent=None):

        super(EditorMainWindow, self).__init__(parent)
        self.ui = Ui_EditorMainWindow()
        self.ui.setupUi(self)
        self.ui.action_open.triggered.connect(self.open_file)

    def open_file(self):
        """ Signal handler for the Open Menu """

        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open File")
        if file_name:
            image = QtGui.QImage(file_name)

            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                                              "Cannot load %s." % file_name)
                return

            array = util.qimage_to_numpy(image)
            garray = util.rgb_to_gray(array)
            self.set_gray_image(garray)

    def set_gray_image(self, gimg):
        """ Sets a 2D grayscale array as the spatial domain image."""

        img = util.gray_to_rgb(gimg)
        qimage = util.numpy_to_qimage(img)
        self.ui.image_label.setPixmap(QPixmap.fromImage(qimage))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    calculator = EditorMainWindow()
    calculator.show()
    sys.exit(app.exec_())
