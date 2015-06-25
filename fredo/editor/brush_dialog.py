from PySide.QtGui import QDialog
from ..gui.brush_dialog import Ui_BrushDialog
from PySide.QtGui import QPixmap
from PySide.QtCore import Qt
from ..brushes import SquareBrush


class BrushDialog(QDialog):

    def __init__(self, parent=None):

        super(BrushDialog, self).__init__(parent)
        self.ui = Ui_BrushDialog()
        self.ui.setupUi(self)

        self.ui.size_slider.valueChanged.connect(self.size_changed)
        self.ui.brush_combo_box.currentIndexChanged.connect(self.brush_changed)
        self.ui.brush_done_btn.clicked.connect(self.select_brush)

        self.ui.brush_combo_box.setCurrentIndex(0)
        self.brush_changed(0)
        self.ui.size_slider.setSliderPosition(10)
        self.selected_brush = None

    def size_changed(self, value):
        "Handle the slider drag event."

        size = self.ui.brush_demo_label.size()
        pixmap = QPixmap(100, 100)
        pixmap.fill(Qt.white)
        cx, cy = int(size.width()/2), int(size.height()/2)
        self.current_brush.set_size(value)
        self.current_brush.draw_marker(cx, cy, pixmap, 1)
        self.ui.brush_demo_label.setPixmap(pixmap)

    def brush_changed(self, index):
        "Handle the brush type change"

        if index == 0:
            self.current_brush = SquareBrush(self.ui.size_slider.value())

    def get_brush(self):
        " Get the selected brush or `None` if dialog was closed. "
        return self.selected_brush

    def select_brush(self):
        " Select the currentently configured brush params "
        self.selected_brush = self.current_brush
        self.close()
