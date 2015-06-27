from abc import ABCMeta, abstractmethod


class BaseBrush:

    __metaclass__ = ABCMeta

    @abstractmethod
    def draw_marker(self, x, y, canvas):
        "Draw the brush marker indicating what area will be painted"
        pass

    @abstractmethod
    def apply(self, x, y, array):
        "Modify the array for the brush to take effect"
        pass

    @abstractmethod
    def set_size(self, size):
        pass

    @abstractmethod
    def set_value(self):
        pass
