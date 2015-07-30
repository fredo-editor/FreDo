from PySide.QtGui import QImage
import numpy as np


def qimage_to_numpy(qimage):
    """ Returns an RGB array given any image. """

    # Each row in a bitmap is stored in the size of multiples of 4
    # If there are less number of bits in a row, it is padded with 0s
    # a 32 bit format ensures that we can get away with dealing with padding
    qimage = qimage.convertToFormat(QImage.Format_ARGB32)
    w, h = qimage.width(), qimage.height()
    string = qimage.bits()

    arr = np.fromstring(bytes(string), dtype=np.uint8)
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
    # On windows, img `img` holds a reference to `string` and behaves wrongly
    # when the string goes out of scope.
    return img.copy()


def rgb_to_gray(arr):
    """ Converts an RGB numpy array to grayscale. """

    r = arr[:, :, 0].astype(np.float)
    g = arr[:, :, 1].astype(np.float)
    b = arr[:, :, 2].astype(np.float)

    garr = 0.299*r + 0.587*g + 0.114*b
    return garr.astype(np.uint8)


def gray_to_rgb(arr):
    """ Converts intensity array to RGB. """

    return np.dstack([arr, arr, arr])


def rgb_to_yuv(arr):
    "Converts RGB array to YUV."

    r = arr[:, :, 0].astype(np.float)
    g = arr[:, :, 1].astype(np.float)
    b = arr[:, :, 2].astype(np.float)

    y = r*.299000 + g*.587000 + b*.114000
    u = r*-.168736 + g*-.331264 + b*.500000 + 128
    v = r*.500000 + g*-.418688 + b*-.081312 + 128

    ret = np.dstack([y, u, v])
    ret = np.clip(ret, 0, 255)
    return ret.astype(np.uint8)


def yuv_to_rgb(arr):
    "Converts YUV array to RGB"

    y = arr[:, :, 0].astype(np.float)
    u = arr[:, :, 1].astype(np.float)
    v = arr[:, :, 2].astype(np.float)

    r = y + 1.4075 * (v - 128)
    g = y - 0.3455 * (u - 128) - (0.7169 * (v - 128))
    b = y + 1.7790 * (u - 128)

    ret = np.dstack([r, g, b])
    ret = np.clip(ret, 0, 255)
    return ret.astype(np.uint8)


def fft_to_qimage(arr):
    """Converts frquency spectrum magnitude image to displayable qimage.

    To make the image visually conceivable, we take the log of the array.
    Otherwise, there is just too much difference between the maxima and minima.
    """

    magnitutde_log = np.log(1 + arr)  # To avoid computing log(0).
    mn = magnitutde_log.min()
    mx = magnitutde_log.max()
    norm_img = 255*(magnitutde_log - mn)/(mx - mn)
    norm_img = norm_img.astype(np.uint8)
    rgb_image = gray_to_rgb(norm_img)
    return numpy_to_qimage(rgb_image)
