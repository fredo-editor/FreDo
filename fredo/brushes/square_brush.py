from .base_brush import BaseBrush
from PySide.QtGui import QPainter
from PySide.QtCore import Qt
import numpy as np


class SquareBrush(BaseBrush):
    " This brush will paint a square and reflect the same diagonally opposite."

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

        self.apply_single(x, y, array)
        h, w = array.shape
        x = w - x
        y = h - y
        self.apply_single(x, y, array)

    def apply_single(self, x, y, array):
        " Apply brush on a single coordinate."

        xa = x - self.size/2
        ya = y - self.size/2
        xa = np.clip(xa, 0, array.shape[1])
        ya = np.clip(ya, 0, array.shape[0])
        xa_end = np.clip(xa + self.size, 0, array.shape[1])
        ya_end = np.clip(ya + self.size, 0, array.shape[0])
        array[ya:ya_end, xa:xa_end] = self.value

    def set_size(self, size):
        self.size = size

    def set_value(self, value):
        self.value = value
