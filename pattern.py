from visual import show_image, save_image, visualize
from cv2 import cv2
from math import ceil
# from progress.bar import ChargingBar
import numpy as np
# import time


def extend_xtimes(image, x):
    h = len(image)
    w = len(image[0])
    image = np.reshape(image, (w * h, 3))
    new_image1 = np.zeros((h * w * x, 3))

    for i in range(h * w * x):
        new_image1[i] = image[i // x].copy()

    new_image1 = np.reshape(new_image1, (h, w * x, 3))
    new_image2 = np.zeros((h * x, w * x, 3))

    for i in range(x * h):
        new_image2[i] = new_image1[i // x].copy()

    return new_image2


"""
Transparency

If putting the pixel with RGBA = (Ra, Ga, Ba, Aa) over the pixel with RGBA = (Rb, Gb, Bb, 100%)
we get the output color equal to (Ra*Aa + Rb*(100% - Aa), Ga*Aa + Gb*(100% - Aa), Ba*Aa + Bb*(100% - Aa), 100%)

Tested with Adobe Photoshop :) Works there
"""
def draw_icon(filepath, image, x, y):
    icon = cv2.imread(filepath, -1)

    y1, y2 = y, y + icon.shape[0]
    x1, x2 = x, x + icon.shape[1]

    alpha_s = icon[:, :, 3] / 255
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        image[y1:y2, x1:x2, c] = (np.multiply(alpha_s, icon[:, :, c]) +
                                  np.multiply(alpha_l, image[y1:y2, x1:x2, c]))

    return image


def multiply_index(i, j, multiplier):
    return i * multiplier, j * multiplier


def draw_lines(image, factor):
    h, w = len(image), len(image[0])
    new_h, new_w = h + 2 * ((h-1) // (10*factor)), w + 2 * ((w-1) // (10*factor))
    new_image = np.zeros((new_h, new_w, 3))

    for i in range(ceil(h / 10*factor)):
        for j in range(ceil(w / 10*factor)):
            y1, x1 = multiply_index(i, j, 10*factor + 2)
            y2, x2 = y1 + 10*factor if y1 + 10*factor < new_h else new_h, \
                     x1 + 10*factor if x1 + 10*factor < new_w else new_w

            old_y1, old_x1 = multiply_index(i, j, 10*factor)
            old_y2, old_x2 = old_y1 + 10*factor if old_y1 + 10*factor < h else h, \
                             old_x1 + 10*factor if old_x1 + 10*factor < w else w

            new_image[y1:y2, x1:x2] = image[old_y1:old_y2, old_x1:old_x2]

    return new_image


def draw_pattern(image, threads):
    factor = 32
    image = extend_xtimes(image, factor)
    h, w = len(image), len(image[0])

    for i in range(0, h, factor):
        for j in range(0, w, factor):
            image = draw_icon('icons/9639.png', image, j, i)  # icons will be changed
            image = draw_icon('icons/border32.png', image, j, i)  # can be added to icons not to waste time

    image = draw_lines(image, factor)

    return image
