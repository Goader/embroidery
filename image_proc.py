from PIL import Image
import numpy as np

"""
Image processing file

Notes:
    - add transfer from HSV, LAB and others to RGB
"""

def get_image(address):
    im = Image.open(address, 'r')

    if im.mode != "RGB":
        raise "Pixels are not in RGB"

    pixels = list(im.getdata())

    width, height = im.size

    print(width, height)

    pixels = np.array_split(pixels, height)

    return pixels, (width, height)


def generate_new_name(address):
    return address[ :address.rfind('.') ] + '_edited.jpg'

def resize_image(address, x, y):
    im = Image.open(address, 'r')
    
    im = im.resize((x, y))

    im.save("tmp.jpg", "JPEG")

    return "tmp.jpg"