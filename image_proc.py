from color_tree import get_thread, get_dmc_tree
from PIL import Image
import numpy as np
import time

"""
Image processing file

Notes:
    - add transfer from HSV, LAB and others to RGB
"""


def get_image(filepath):
    im = Image.open(filepath, 'r')

    if im.mode != "RGB":
        raise Exception("Pixels are not in RGB")

    pixels = list(im.getdata())
    width, height = im.size

    pixels = np.array_split(pixels, height)
    return pixels, (width, height)


def resize_image(filepath, x, y):
    im = Image.open(filepath, 'r')
    im = im.resize((x, y))
    im.save("tmp.jpg", "JPEG")
    return "tmp.jpg"


# Applies Floyd Steinberg effect on the particular pixel
def floyd_steinberg_effect(image, x, y, quant_err, coef):
    for i in range(3):
        image[x][y][i] += quant_err[i] * coef
        image[x][y][i] = round(max(0, min(255, image[x][y][i])))


def valid_idx(x, y, w, h):
    return 0 <= x < w and y >= 0 and y < h


# Iterates neighbors with the given coefficient for 
# Floyd Steinberg's effect
def iterate_neighbors(x, y, w, h):
    if valid_idx(x + 1, y, w, h):
        yield x + 1, y, 7 / 16

    if valid_idx(x, y + 1, w, h):
        yield x, y + 1, 5 / 16

    if valid_idx(x + 1, y + 1, w, h):
        yield x + 1, y + 1, 1 / 16

    if valid_idx(x - 1, y + 1, w, h):
        yield x - 1, y + 1, 3 / 16


# Selecting appropriate threads
def process_image(pixels, w, h):
    tree, dmcs, idxs = get_dmc_tree()

    image = pixels
    threads = []

    t0 = time.time()

    # ts = []

    for y in range(h):
        for x in range(w):
            # Getting thread and its RGB tuple
            thread, rgb = get_thread(image[x][y], tree, idxs, dmcs)
            threads.append(thread)

            # Recreating the output image
            image[x][y] = rgb

            # if thread not in ts:
            #     ts.append(thread)

            # Applying Floyd Steinberg's algorithm, by affecting neighbors
            quant_error = [(image[x][y][i] - rgb[i]) for i in range(3)]
            for nx, ny, coef in iterate_neighbors(x, y, w, h):
                floyd_steinberg_effect(image, nx, ny, quant_error, coef)

    print("\nTime spent: ", round(time.time() - t0, 2))
    # print("Distinct threads used: ", len(ts))

    threads = np.array_split(threads, w)

    return image.transpose(1, 0, 2), threads
