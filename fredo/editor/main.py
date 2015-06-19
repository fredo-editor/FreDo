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
        self.ui.image_zoom_in_btn.clicked.connect(self.image_zoom_in)
        self.ui.image_zoom_out_btn.clicked.connect(self.image_zoom_out)

        self.spatial_array = None
        self.scale = 1.0

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
            self.spatial_array = garray
            self.set_gray_image(garray)

    def set_gray_image(self, gimg):
        """ Sets a 2D grayscale array as the spatial domain image."""

        img = util.gray_to_rgb(gimg)
        qimage = util.numpy_to_qimage(img)
        w, h = qimage.width(), qimage.height()
        sw, sh = int(w*self.scale), int(h*self.scale)
        pixmap = QPixmap.fromImage(qimage)
        scaled_pixmap = pixmap.scaled(sw, sh)
        self.ui.image_label.setPixmap(scaled_pixmap)

    def image_zoom_in(self):
        " Zoom in the spatial domain image "

        if self.spatial_array is None:
            return

        self.scale += 0.1
        self.set_gray_image(self.spatial_array)

    def image_zoom_out(self):
        " Zoom out the spatial domain image "

        if self.spatial_array is None:
            return

        self.scale -= 0.1
        self.set_gray_image(self.spatial_array)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    calculator = EditorMainWindow()
    calculator.show()
    sys.exit(app.exec_())
