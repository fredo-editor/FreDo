from ..gui.main_window import Ui_EditorMainWindow
from PySide.QtGui import QApplication, QMainWindow, QPixmap
from PySide import QtGui, QtCore
from PySide.QtCore import QObject
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

        self.freq_pixmap = None
        self.scaled_freq_pixmap = None
        self.image_pixmap = None
        self.scaled_image_pixmap = None

        self.spatial_scale = 1.0
        self.frequency_scale = 1.0

        self.current_brush = None

    def open_file(self):
        """ Signal handler for the Open Menu """

        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open File")[0]
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

        pixmap = QPixmap.fromImage(qimage)
        self.set_freq_pixmap(pixmap)
        self.invalidate_freq_scale()
        self.render_freq()

    def set_freq_pixmap(self, pixmap):
        "Sets the pixmap to be shown for frequency image"

        self.freq_pixmap = pixmap

    def invalidate_freq_scale(self):
        "Implies scale has changed and recomputes internal fields"

        w, h = self.freq_pixmap.width(), self.freq_pixmap.height()
        sw, sh = int(w*self.frequency_scale), int(h*self.frequency_scale)
        self.scaled_freq_pixmap = self.freq_pixmap.scaled(sw, sh)

    def render_freq(self, pixmap=None):
        """Render the pixmap as spatial image. If not given, display last known
        sclaed spatial image pixmap.

        Will mostly be called without 2nd argument. When a brush is set, we use
        the scaled frequency pixmap, draw the brush and supply it as `pixmap`
        to be shown.
        """

        if not pixmap:
            pixmap = self.scaled_freq_pixmap

        self.ui.freq_label.setPixmap(pixmap)

    def set_freq_image_angle(self, fimg):
        " Sets a numpy array as a frequncy domain image magnitude. "

        self.frequency_array_angle = fimg

    def set_gray_image(self, gimg):
        """ Sets a 2D grayscale array as the spatial domain image."""

        self.spatial_array = gimg
        img = util.gray_to_rgb(gimg)
        qimage = util.numpy_to_qimage(img)
        pixmap = QPixmap.fromImage(qimage)
        self.set_image_pixmap(pixmap)
        self.invalidate_image_scale()
        self.render_image()

    def set_image_pixmap(self, pixmap):
        "Sets the pixmap to be shown for spatial image"

        self.image_pixmap = pixmap

    def invalidate_image_scale(self):
        "Implies scale has changed and recomputes internal fields"

        w, h = self.image_pixmap.width(), self.image_pixmap.height()
        sw, sh = int(w*self.spatial_scale), int(h*self.spatial_scale)
        self.scaled_image_pixmap = self.image_pixmap.scaled(sw, sh)

    def render_image(self, pixmap=None):
        """Render the pixmap as spatial image. If not given, display last known
        sclaed spatial image pixmap
        """

        if not pixmap:
            pixmap = self.scaled_image_pixmap

        self.ui.image_label.setPixmap(pixmap)

    def image_zoom_in(self):
        " Zoom in the spatial domain image "

        if self.spatial_array is None:
            return

        self.spatial_scale += 0.1
        self.invalidate_image_scale()
        self.render_image()

    def image_zoom_out(self):
        " Zoom out the spatial domain image "

        if self.spatial_array is None:
            return

        self.spatial_scale -= 0.1
        self.invalidate_image_scale()
        self.render_image()

    def freq_zoom_out(self):
        "Zoom out the frequency domain image."

        if self.frequency_array_magnitude is None:
            return

        self.frequency_scale -= 0.1
        self.invalidate_freq_scale()
        self.render_freq()

    def freq_zoom_in(self):
        "Zoom out the frequency domain image."

        if self.frequency_array_magnitude is None:
            return

        self.frequency_scale += 0.1
        self.invalidate_freq_scale()
        self.render_freq()

    def handle_image_move(self, event):
        "Handle mouse move on the spatial image."

        if self.spatial_array is None:
            return

        self.handle_image_stats(event)

    def handle_image_stats(self, event):
        """Given an event, take care of displaying stats for spatial image.

        The assumption made here is that the QLabel is exactly the size of the
        image.
        """
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
        """Handle mouse move on the frequency domain image.

        The assumption made here is that the QLabel is exactly the size of the
        image.
        """

        if self.frequency_array_magnitude is None:
            return

        self.handle_freq_stats(event)

        if self.current_brush:
            pixmap = self.scaled_freq_pixmap.copy()
            self.current_brush.draw_marker(event.x(), event.y(), pixmap,
                                           self.frequency_scale)
            self.render_freq(pixmap)

    def handle_freq_stats(self, event):
        "Given an event, show frequency image stats"
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
        d = BrushDialog(self)
        d.exec_()
        if d.get_brush():
            self.current_brush = d.get_brush()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    editor = EditorMainWindow()
    editor.show()
    sys.exit(app.exec_())
