
"""
For each function:
image   = array of pixel intensities in 2 or 3 dimensions
returns = array of pixel intensities same shape as `image`
"""

from scipy.ndimage import rotate, interpolation
import numpy as np
import matplotlib.pyplot as plt
from Utils import Util
import numpy as np
# import pandas as pd
import cv2
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt


def scaleit(image, factor, isseg=False):
    order = 0 if isseg == True else 3

    height, width, depth = image.shape
    zheight = int(np.round(factor * height))
    zwidth = int(np.round(factor * width))

    if factor < 1.0:
        newimg = np.zeros_like(image)
        row = int((height - zheight) / 2)
        col = int((width - zwidth) / 2)
        newimg[row:row + zheight, col:col + zwidth, :] = interpolation.zoom(image, (float(factor), float(factor), 1.0),
                                                                            order=order, mode='nearest')[0:zheight,
                                                         0:zwidth, :]

        return newimg

    elif factor > 1.0:
        row = (zheight - height) // 2
        col = (zwidth - width) // 2

        newimg = interpolation.zoom(image[row:row + zheight, col:col + zwidth], (float(factor), float(factor), 1.0),
                                    order=order, mode='nearest')

        extrah = (newimg.shape[0] - height) // 2
        extraw = (newimg.shape[1] - width) // 2
        newimg = newimg[extrah:extrah + height, extraw:extraw + width, :]

        return newimg

    else:
        return image


def resampleit(image, dims, isseg=False):
    order = 0 if isseg == True else 5

    image = interpolation.zoom(image, np.array(dims) / np.array(image.shape, dtype=np.float32), order=order,
                               mode='nearest')

    if isseg:
        image[np.where(image == 4)] = 3

    return image if isseg else (image - image.min()) / (image.max() - image.min())


def translateit(image, offset, isseg=False, mode='nearest'):
    order = 0 if isseg else 5
    mode = 'nearest' if isseg else 'mirror'
    offset = offset if image.ndim == 2 else (int(offset[0]), int(offset[1]), 0)

    return interpolation.shift(image, offset, order=order)


def rotateit(image, theta, ax):
    #    order = 0 if isseg == True else 5

    return rotate(image, float(theta), reshape=False, axes=ax)


def flipit(image, axes):
    if axes[0]:
        image = np.fliplr(image)
    if axes[1]:
        image = np.flipud(image)

    return image


def intensifyit(image, factor):
    return image * float(factor)


def cropit(image, seg=None, margin=5):
    shortaxis = np.argmin(image.shape[:2])
    trimaxes = 0 if shortaxis == 1 else 1

    trim = image.shape[shortaxis]
    center = image.shape[trimaxes] // 2
    lrcenter = image.shape[shortaxis] // 2

    if seg is not None:

        hits = np.where(seg != 0)
        mins = np.amin(hits, axis=1)
        maxs = np.amax(hits, axis=1)
        segtrim = max(maxs - mins) + margin

        trim = segtrim
        center = np.mean(hits, 1, dtype=int)[0]
        lrcenter = np.mean(hits, 1, dtype=int)[1]

        if center - (trim // 2) > mins[0]:
            while center - (trim // 2) > mins[0]:
                center = center - 1
            center = center

        if center + (trim // 2) < maxs[0]:
            while center + (trim // 2) < maxs[0]:
                center = center + 1
            center = center

        if lrcenter - (trim // 2) > mins[1]:
            while lrcenter - (trim // 2) > mins[1]:
                lrcenter = lrcenter - 1
            lrcenter = lrcenter

        if lrcenter + (trim // 2) < maxs[1]:
            while lrcenter + (trim // 2) < maxs[1]:
                lrcenter = lrcenter + 1
            lrcenter = lrcenter

    top = max(0, center - (trim // 2) - margin // 2)
    bottom = trim + margin if top == 0 else top + trim + (margin // 2)
    left = max(0, lrcenter - (trim // 2) - margin // 2)
    right = trim + margin if left == 0 else left + trim + (margin // 2)

    image[center - 5:center + 5, lrcenter - 5:lrcenter + 5, :] = 255
    image[top:bottom, left - 2:left + 2, :] = 255
    image[top:bottom, right - 2:right + 2, :] = 255
    image[top - 2:top + 2, left:right, :] = 255
    image[bottom - 2:bottom + 2, left:right, :] = 255

    if bottom > image.shape[trimaxes]:
        bottom = image.shape[trimaxes]
        top = bottom - trim

    if right > image.shape[shortaxis]:
        right = image.shape[shortaxis]
        left = right - trim

    image = image[top: bottom, left:right, :]

    if seg is not None:
        seg = seg[top: bottom, left:right]

        return image, seg
    else:
        return image


'''Only works for 3D images... i.e. slice-wise'''


def sliceshift(image, shift_min=-3, shift_max=3, fraction=0.5, isseg=False):
    newimage = image
    numslices = np.random.randint(1, int(image.shape[-1] * fraction) + 1, 1, dtype=int)
    slices = np.random.randint(0, image.shape[-1], numslices, dtype=int)
    for slc in slices:
        offset = np.random.randint(shift_min, shift_max, 2, dtype=int)
        newimage[:, :, slc] = translateit(image[:, :, slc], offset, isseg=isseg)

    return newimage


#


# Function to distort image
def elastic_transform(image, alpha, sigma, alpha_affine, random_state=None):
    """Elastic deformation of images as described in [Simard2003]_ (with modifications).
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
         Convolutional Neural Networks applied to Visual Document Analysis", in
         Proc. of the International Conference on Document Analysis and
         Recognition, 2003.

     Based on https://gist.github.com/erniejunior/601cdf56d2b424757de5
    """
    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = image.shape
    shape_size = shape[:2]

    # Random affine
    center_square = np.float32(shape_size) // 2
    square_size = min(shape_size) // 3
    pts1 = np.float32([center_square + square_size, [center_square[0] + square_size, center_square[1] - square_size],
                       center_square - square_size])
    pts2 = pts1 + random_state.uniform(-alpha_affine, alpha_affine, size=pts1.shape).astype(np.float32)
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, shape_size[::-1], borderMode=cv2.BORDER_REFLECT_101)

    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dz = np.zeros_like(dx)

    x, y, z = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]), np.arange(shape[2]))
    indices = np.reshape(y + dy, (-1, 1)), np.reshape(x + dx, (-1, 1)), np.reshape(z, (-1, 1))

    return map_coordinates(image, indices, order=1, mode='reflect').reshape(shape)


# Define function to draw a grid
def draw_grid(im, grid_size):
    # Draw grid lines
    for i in range(0, im.shape[1], grid_size):
        cv2.line(im, (i, 0), (i, im.shape[0]), color=(255,))
    for j in range(0, im.shape[0], grid_size):
        cv2.line(im, (0, j), (im.shape[1], j), color=(255,))

