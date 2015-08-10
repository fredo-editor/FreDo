from PySide import QtCore
import numpy as np


class IFTThread(QtCore.QThread):
    """ Computes the inverse fourier transform used to render image.

    After completion the thread emits its `ifft_done(arr)` signal where `arr`
    is the 2D grayscale Y component.
    """

    ift_done = QtCore.Signal(np.ndarray)

    def __init__(self, magnitude, angle):
        """ Initialize with magnitude and angle of transform.

        Both are assumed to be shifted (highest frequency in the center).
        """

        QtCore.QThread.__init__(self)
        self.magnitude = magnitude
        self.angle = angle

    def run(self):
        r = np.fft.ifftshift(self.magnitude)
        theta = np.fft.ifftshift(self.angle)
        real = r*np.cos(theta)
        imag = r*np.sin(theta)

        fft_image = real + 1j*imag
        image = np.fft.ifft2(fft_image)

        image = np.real(image)
        mx, mn = image.max(), image.min()
        image = 255*(image - mn)/(mx - mn)
        image = image.astype(np.uint8)
        self.ift_done.emit(image)
