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
        self.ui.action_save_spatial.triggered.connect(self.save_spatial)
        self.ui.action_brush.triggered.connect(self.show_brush)
        self.ui.action_none.triggered.connect(self.remove_brush)
        self.ui.image_zoom_in_btn.clicked.connect(self.image_zoom_in)
        self.ui.image_zoom_out_btn.clicked.connect(self.image_zoom_out)
        self.ui.freq_zoom_in_btn.clicked.connect(self.freq_zoom_in)
        self.ui.freq_zoom_out_btn.clicked.connect(self.freq_zoom_out)
        self.ui.image_label.installEventFilter(self)
        self.ui.freq_label.installEventFilter(self)

        self.ui.image_label.setMouseTracking(True)
        self.ui.freq_label.setMouseTracking(True)

        self.spatial_image = None
        # This will store the shifted frequency image
        self.frequency_array_magnitude = None
        self.frequency_array_angle = None

        self.freq_pixmap = None
        self.scaled_freq_pixmap = None
        self.image_pixmap = None
        self.scaled_image_pixmap = None

        self.spatial_scale = 1.0
        self.frequency_scale = 1.0

        self.current_brush = None

    def open_file(self):
        """ Signal handler for the Open Menu """

        filters = "Image Files (*.png *.jpg *.bmp)"
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                                                      filter=filters)[0]
        if file_name:
            image = QtGui.QImage(file_name)
            filters = "Image Files (*.png *.jpg *.bmp)"

            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                                              "Cannot load %s." % file_name)
                return

            array = util.qimage_to_numpy(image)
            image = util.rgb_to_yuv(array)
            garray = image[..., 0]
            farray = np.fft.fft2(garray)
            farray = np.fft.fftshift(farray)

            self.set_yuv_image(image)
            self.set_freq_image_angle(np.angle(farray))
            self.set_freq_image_magnitude(np.absolute(farray))

    def set_freq_image_magnitude(self, fimg):
        """ Sets a numpy array as a frequncy domain image magnitude.

        This function expects an appropriately shifted numpy array as input.
        Except taking log, no manipulation to the values is done before
        rendering. The function updates recomputes all internal intermediate
        values and re renders the frequency UI.
        """

        self.frequency_array_magnitude = fimg
        qimage = util.fft_to_qimage(self.frequency_array_magnitude)

        pixmap = QPixmap.fromImage(qimage)
        self.set_freq_pixmap(pixmap)
        self.invalidate_freq_scale()
        self.render_freq()

    def set_freq_pixmap(self, pixmap):
        """Sets the pixmap to be shown for frequency image.

        This function only caches the pixmap, not computation or UI updation
        is done.
        """

        self.freq_pixmap = pixmap

    def invalidate_freq_scale(self):
        """Implies scale has changed and recomputes internal fields

        This function is to be called when either `self.freq_pixmap` changes
        or `self.frequency_scale` changes. This function merely caches the
        scaled pixmap, no UI updation is done.
        """

        w, h = self.freq_pixmap.width(), self.freq_pixmap.height()
        sw, sh = int(w*self.frequency_scale), int(h*self.frequency_scale)
        self.scaled_freq_pixmap = self.freq_pixmap.scaled(sw, sh)

    def render_freq(self, pixmap=None):
        """Render `pixmap` as the frequency image. If not given display last
        known sclaed spatial image pixmap.

        This function does not perform any computations internally. The
        function is to be called to update the UI to reflect the state of the
        internal fields, when called without the 2nd argument. When a brush
        is set, a pixmap with the brush drawn on it can supplied as the 2nd
        argument.
        """

        if not pixmap:
            pixmap = self.scaled_freq_pixmap

        self.ui.freq_label.setPixmap(pixmap)

    def set_freq_image_angle(self, fimg):
        " Sets a numpy array as a frequncy domain image angle. "

        self.frequency_array_angle = fimg

    def set_yuv_image(self, img):
        """ Sets the spatial image as YUV array.

        The function expects a `uint8` array and will set the spatial domain
        image in the UI along with updating all internal fields.
        """

        self.spatial_image = img
        img = util.yuv_to_rgb(self.spatial_image)
        qimage = util.numpy_to_qimage(img)
        pixmap = QPixmap.fromImage(qimage)
        self.set_image_pixmap(pixmap)
        self.invalidate_image_scale()
        self.render_image()

    def set_image_pixmap(self, pixmap):
        """Sets the pixmap to be shown for spatial image.

        This function only caches the pixmap, not computation or UI updation
        is done.
        """

        self.image_pixmap = pixmap

    def invalidate_image_scale(self):
        """Implies scale has changed and recomputes internal fields.

        This function is to be called when either `self.image_pixmap` changes
        or `self.spatial_scale` changes. This function merely caches the
        scaled pixmap, no UI updation is done.
        """

        w, h = self.image_pixmap.width(), self.image_pixmap.height()
        sw, sh = int(w*self.spatial_scale), int(h*self.spatial_scale)
        self.scaled_image_pixmap = self.image_pixmap.scaled(sw, sh)

    def render_image(self, pixmap=None):
        """Render the pixmap as spatial image. If not given, display last known
        sclaed spatial image pixmap.
        """

        if not pixmap:
            pixmap = self.scaled_image_pixmap

        self.ui.image_label.setPixmap(pixmap)

    def image_zoom_in(self):
        " Zoom in the spatial domain image "

        if self.spatial_image is None:
            return

        self.spatial_scale += 0.1
        self.invalidate_image_scale()
        self.render_image()

    def image_zoom_out(self):
        " Zoom out the spatial domain image "

        if self.spatial_image is None:
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

        if self.spatial_image is None:
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

        r = np.clip(r, 0, self.spatial_image.shape[0])
        c = np.clip(c, 0, self.spatial_image.shape[1])
        value = self.spatial_image[r, c].astype(np.int)

        msg = "X:%d Y:%d Value:" % (x, y)
        msg += str(value)
        self.ui.image_info_label.setText(msg)

    def handle_freq_move(self, event):
        """Handle mouse move on the frequency domain image.

        """

        if self.frequency_array_magnitude is None:
            return

        self.handle_freq_stats(event)

        if self.current_brush:
            pixmap = self.scaled_freq_pixmap.copy()
            self.current_brush.draw_marker(event.x(), event.y(), pixmap,
                                           self.frequency_scale)
            # We use the pre computed scaled pixmap and mark the brush on it
            # before displaying
            self.render_freq(pixmap)

    def handle_freq_stats(self, event):
        """Given an event, show frequency image stats.

        The assumption made here is that the QLabel is exactly the size of the
        image.
        """
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
        "Call to handle relevant events."

        if obj == self.ui.image_label:
            if event.type() == QtCore.QEvent.MouseMove:
                self.handle_image_move(event)
                return True

        elif obj == self.ui.freq_label:
            if event.type() == QtCore.QEvent.MouseMove:
                self.handle_freq_move(event)
                return True
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    self.handle_freq_click(event)

        return QObject.eventFilter(self, obj, event)

    def handle_freq_click(self, event):
        "Handle the click on the frequency image."

        if not self.current_brush is None:

            x, y = event.x(), event.y()
            x /= self.frequency_scale
            y /= self.frequency_scale
            h, w = self.frequency_array_magnitude.shape

            self.current_brush.apply(x, y, self.frequency_array_magnitude)

            self.set_freq_image_magnitude(self.frequency_array_magnitude)
            self.render_freq()
            self.recompute_spatial_image()

    def show_brush(self):
        "Show the brush dialog box."
        d = BrushDialog(self)
        d.exec_()
        if d.get_brush():
            self.current_brush = d.get_brush()

    def remove_brush(self):
        "Deselcts a brush."
        self.current_brush = None
        self.render_freq()

    def recompute_spatial_image(self):
        "Recompute the spatial image from the frequency image and render it."

        r = np.fft.ifftshift(self.frequency_array_magnitude)
        theta = np.fft.ifftshift(self.frequency_array_angle)
        real = r*np.cos(theta)
        imag = r*np.sin(theta)

        fft_image = real + 1j*imag
        image = np.fft.ifft2(fft_image)

        image = np.real(image)
        mx, mn = image.max(), image.min()
        image = 255*(image - mn)/(mx - mn)
        image = image.astype(np.uint8)
        self.spatial_image[:, :, 0] = image
        self.set_yuv_image(self.spatial_image)

    def save_spatial(self):

        if self.spatial_image is None:
            QtGui.QMessageBox.information(self, "Error", "No Image to Save")
            return

        filters = "Image Files (*.png)"
        filename = QtGui.QFileDialog.getSaveFileName(self, "Save Image",
                                                     filter=filters)[0]

        if not filename.lower().endswith('.png'):
            filename += '.png'

        arr = util.yuv_to_rgb(self.spatial_image)
        image = util.numpy_to_qimage(arr)
        success = image.save(filename)

        if not success:
            msg = "Could not save image at the location."
            QtGui.QMessageBox.information(self, "Error", msg)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    editor = EditorMainWindow()
    editor.show()
    sys.exit(app.exec_())
