from PIL import Image
import numpy as np

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
    print(width, height)
    pixels = np.array_split(pixels, height)
    return pixels, (width, height)


def generate_new_name(filepath):
    return filepath[:filepath.rfind(".")] + "_edited.jpg"


def resize_image(filepath, x, y):
    im = Image.open(filepath, 'r')
    im = im.resize((x, y))
    im.save("tmp.jpg", "JPEG")
    return "tmp.jpg"
