from PyQt4.QtGui import QImage
import numpy as np


def qimage_to_numpy(qimage):
    """ Returns an RGB array given any image. """

    # Each row in a bitmap is stored in the size of multiples of 4
    # If there are less number of bits in a row, it is padded with 0s
    # a 32 bit format ensures that we can get away with dealing with padding
    qimage = qimage.convertToFormat(QImage.Format_ARGB32)
    w, h = qimage.width(), qimage.height()
    string = qimage.bits().asstring(qimage.numBytes())

    arr = np.fromstring(string, dtype=np.uint8)
    arr = arr.reshape(h, w, 4)
    arr = arr[..., 0:3]

    c0 = arr[..., 0].copy()
    c2 = arr[..., 2].copy()

    arr[..., 0] = c2
    arr[..., 2] = c0
    return arr


def numpy_to_qimage(array):
    """ Returns QImage from an RGB array ."""

    rows, cols, channels = array.shape
    array4 = np.zeros((rows, cols, 4), dtype=np.uint8)
    array4[..., 0:3] = array
    array4[..., 3] = 255

    c0 = array[..., 0].copy()
    c2 = array[..., 2].copy()

    array4[..., 0] = c2
    array4[..., 2] = c0

    string = array4.tostring()

    img = QImage(string, cols, rows, QImage.Format_ARGB32)
    return img
