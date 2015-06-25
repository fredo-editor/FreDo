from .base_brush import BaseBrush
from PySide.QtGui import QPainter
from PySide.QtCore import Qt


class SquareBrush(BaseBrush):

    def __init__(self, size=1):
        self.size = size

    def draw_marker(self, x, y, pixmap, scale):
        "Draw the brush marker indicating what area will be painted"

        w, h = self.size*scale, self.size*scale
        painter = QPainter(pixmap)

        painter.setPen(Qt.red)
        painter.drawRect(x - w/2, y - h/2, w, h)

    def apply(self, x, y, array):
        "Modify the array for the brush to take effect"
        pass

    def set_size(self, size):
        self.size = size

    def get_size(self):
        pass
