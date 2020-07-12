from image_proc import get_image, resize_image, process_image
from visual import visualize
import numpy as np
import os


address = input("Input image file path: ")
x = int(input("Type in width:  "))
y = int(input("Type in height: "))

new_address = resize_image(address, x, y)

pixels, size = get_image(new_address)
pixels = np.array(pixels)
pixels = pixels.transpose(1, 0, 2)
w, h = size

if w != x or h != y:
    raise Exception("Dimensions collapse")

image, threads = process_image(pixels, w, h)

visualize(image, address)

os.remove("tmp.jpg")