from abc import ABCMeta, abstractmethod

class BaseBrush:

    __metaclass__ = ABCMeta

    @abstractmethod
    def draw_marker(self, x, y, canvas):
        "Draw the brush marker indicating what area will be painted"
        pass

    def apply(self, x, y, array):
        "Modify the array for the brush to take effect"
