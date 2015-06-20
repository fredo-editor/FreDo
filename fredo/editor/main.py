from ..gui.main_window import Ui_EditorMainWindow
from PyQt4.QtGui import QApplication, QMainWindow, QPixmap
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import sys
import numpy as np
from .. import util
from .brush_dialog import BrushDialog


class EditorMainWindow(QMainWindow):

    def __init__(self, parent=None):

        super(EditorMainWindow, self).__init__(parent)
        self.ui = Ui_EditorMainWindow()
        self.ui.setupUi(self)

        self.ui.action_open.triggered.connect(self.open_file)
        self.ui.action_brush.triggered.connect(self.show_brush)
        self.ui.image_zoom_in_btn.clicked.connect(self.image_zoom_in)
        self.ui.image_zoom_out_btn.clicked.connect(self.image_zoom_out)
        self.ui.freq_zoom_in_btn.clicked.connect(self.freq_zoom_in)
        self.ui.freq_zoom_out_btn.clicked.connect(self.freq_zoom_out)
        self.ui.image_label.installEventFilter(self)
        self.ui.freq_label.installEventFilter(self)

        self.ui.image_label.setMouseTracking(True)
        self.ui.freq_label.setMouseTracking(True)

        self.spatial_array = None
        # This will store the shifted frequency image
        self.frequency_array_magnitude = None
        self.frequency_array_agnle = None
        self.spatial_scale = 1.0
        self.frequency_scale = 1.0

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
            farray = np.fft.fft2(garray)
            farray = np.fft.fftshift(farray)

            self.set_gray_image(garray)
            self.set_freq_image_angle(np.angle(farray))
            self.set_freq_image_magnitude(np.absolute(farray))

    def set_freq_image_magnitude(self, fimg):
        " Sets a numpy array as a frequncy domain image magnitude. "

        self.frequency_array_magnitude = fimg
        qimage = util.fft_to_qimage(self.frequency_array_magnitude)
        w, h = qimage.width(), qimage.height()
        sw, sh = int(w*self.frequency_scale), int(h*self.frequency_scale)
        pixmap = QPixmap.fromImage(qimage)
        scaled_pixmap = pixmap.scaled(sw, sh)
        self.ui.freq_label.setPixmap(scaled_pixmap)

    def set_freq_image_angle(self, fimg):
        " Sets a numpy array as a frequncy domain image magnitude. "

        self.frequency_array_angle = fimg

    def set_gray_image(self, gimg):
        """ Sets a 2D grayscale array as the spatial domain image."""

        self.spatial_array = gimg
        img = util.gray_to_rgb(gimg)
        qimage = util.numpy_to_qimage(img)
        w, h = qimage.width(), qimage.height()
        sw, sh = int(w*self.spatial_scale), int(h*self.spatial_scale)
        pixmap = QPixmap.fromImage(qimage)
        scaled_pixmap = pixmap.scaled(sw, sh)
        self.ui.image_label.setPixmap(scaled_pixmap)

    def image_zoom_in(self):
        " Zoom in the spatial domain image "

        if self.spatial_array is None:
            return

        self.spatial_scale += 0.1
        self.set_gray_image(self.spatial_array)

    def image_zoom_out(self):
        " Zoom out the spatial domain image "

        if self.spatial_array is None:
            return

        self.spatial_scale -= 0.1
        self.set_gray_image(self.spatial_array)

    def freq_zoom_out(self):
        "Zoom out the frequency domain image."

        if self.frequency_array_magnitude is None:
            return

        self.frequency_scale -= 0.1
        self.set_freq_image_magnitude(self.frequency_array_magnitude)

    def freq_zoom_in(self):
        "Zoom out the frequency domain image."

        if self.frequency_array_magnitude is None:
            return

        self.frequency_scale += 0.1
        self.set_freq_image_magnitude(self.frequency_array_magnitude)

    def handle_image_move(self, event):
        "Handle mouse move on the spatial image."

        if self.spatial_array is None:
            return

        pos = event.pos()
        x, y = pos.x(), pos.y()
        x, y = int(x/self.spatial_scale), int(y/self.spatial_scale)
        r, c = y, x

        r = np.clip(r, 0, self.spatial_array.shape[0])
        c = np.clip(c, 0, self.spatial_array.shape[1])
        value = self.spatial_array[r, c]

        msg = "X:%d Y:%d Value:%d" % (x, y, value)
        self.ui.image_info_label.setText(msg)

    def handle_freq_move(self, event):
        "Handle mouse move on the frequency domain image."

        if self.frequency_array_magnitude is None:
            return

        pos = event.pos()
        x, y = pos.x(), pos.y()
        x, y = int(x/self.frequency_scale), int(y/self.frequency_scale)
        r, c = y, x

        r = np.clip(r, 0, self.frequency_array_magnitude.shape[0])
        c = np.clip(c, 0, self.frequency_array_magnitude.shape[1])
        value = self.frequency_array_magnitude[r, c]

        msg = "X:%d Y:%d Value:%d" % (x, y, value)
        self.ui.freq_info_label.setText(msg)

    def eventFilter(self, obj, event):

        if obj == self.ui.image_label:
            if event.type() == QtCore.QEvent.MouseMove:
                self.handle_image_move(event)
                return True

        elif obj == self.ui.freq_label:
            if event.type() == QtCore.QEvent.MouseMove:
                self.handle_freq_move(event)
                return True

        return QObject.eventFilter(self, obj, event)

    def show_brush(self):
        print("Square Brush")
        d = BrushDialog(self)
        d.exec_()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    editor = EditorMainWindow()
    editor.show()
    sys.exit(app.exec_())
