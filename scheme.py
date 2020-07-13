from visual import show_image, save_image, visualize
from cv2 import cv2
from math import ceil
import numpy as np


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

def draw_icon(filepath, image, x, y):
    icon = cv2.imread(filepath, -1)

    y1, y2 = y, y + icon.shape[0]
    x1, x2 = x, x + icon.shape[1]

    alpha_s = icon[:, :, 3] // 255
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        image[y1:y2, x1:x2, c] = (np.multiply(alpha_s, icon[:, :, c]) +
                                  np.multiply(alpha_l, image[y1:y2, x1:x2, c]))

    return image

def new_square_index(i, j):
    return i * 172, j * 172

def old_square_index(i, j):
    return i * 170, j * 170

def draw_lines(image):
    h, w = len(image), len(image[0])
    new_h, new_w = h + 2*((h - 1)//170), w + 2*((w - 1)//170)
    new_image = np.zeros((new_h, new_w, 3))

    for i in range(ceil(h / 170)):
        for j in range(ceil(w / 170)):
            y1, x1 = new_square_index(i, j)
            y2, x2 =    y1 + 170 if y1 + 170 < new_h else new_h, \
                        x1 + 170 if x1 + 170 < new_w else new_w

            old_y1, old_x1 = old_square_index(i, j)
            old_y2, old_x2 =    old_y1 + 170 if old_y1 + 170 < h else h, \
                                old_x1 + 170 if old_x1 + 170 < w else w

            new_image[y1:y2, x1:x2] = image[old_y1:old_y2, old_x1:old_x2]

    return new_image

def draw_scheme(image, threads):
    image = extend_xtimes(image, 17)
    h, w = len(image), len(image[0])

    for i in range(0, h, 17):
        for j in range(0, w, 17):
            image = draw_icon('icons/test.png',   image, j + 3, i + 3) # icons will be changed
            image = draw_icon('icons/border.png', image, j, i) # can be added to icons not to waste time
                                            
    image = draw_lines(image)

    return image