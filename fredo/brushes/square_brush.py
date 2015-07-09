from .base_brush import BaseBrush
from PySide.QtGui import QPainter
from PySide.QtCore import Qt


class SquareBrush(BaseBrush):

    def __init__(self, size=1, value=0):
        self.size = size
        self.value = value

    def draw_marker(self, x, y, pixmap, scale):
        "Draw the brush marker indicating what area will be painted"

        w, h = self.size*scale, self.size*scale
        painter = QPainter(pixmap)

        painter.setPen(Qt.green)
        painter.drawRect(x - w/2, y - h/2, w, h)

        x = pixmap.width() - x
        y = pixmap.height() - y
        painter.drawRect(x - w/2, y - h/2, w, h)

    def apply(self, x, y, array):
        "Modify the array for the brush to take effect"

        xa = x - self.size/2
        ya = y - self.size/2
        array[ya:ya+self.size, xa:xa+self.size] = self.value

        h, w = array.shape
        x = w - x
        y = h - y
        xa = x - self.size/2
        ya = y - self.size/2
        array[ya:ya+self.size, xa:xa+self.size] = self.value

    def set_size(self, size):
        self.size = size

    def set_value(self, value):
        self.value = value
