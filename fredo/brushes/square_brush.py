from .base_brush import BaseBrush
from PySide.QtGui import QPainter
from PySide.QtCore import Qt


class SquareBrush(BaseBrush):

    def __init__(self, size=1):
        self.size = size

    def draw_marker(self, x, y, pixmap):
        "Draw the brush marker indicating what area will be painted"

        size = pixmap.size()
        w, h = size.width(), size.height()
        cx, cy = int(w/2), int(h/2)
        painter = QPainter(pixmap)

        painter.setPen(Qt.red)
        painter.drawRect(cx - self.size/2, cy - self.size/2,
                         self.size, self.size)

    def apply(self, x, y, array):
        "Modify the array for the brush to take effect"
        pass

    def set_size(self, size):
        self.size = size

    def get_size(self):
        pass
