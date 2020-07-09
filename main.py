from color_tree import get_thread, get_dmc_tree, get_thread_info
from image_proc import get_image, resize_image
from visual import visualize
from progress.bar import ChargingBar
import numpy as np
import os
import time


address = str( input("Input image address: ") )
x = int( input("Type in width:  ") )
y = int( input("Type in height: ") )

new_address = resize_image(address, x, y)

pixels, size = get_image(new_address)
w, h = size

if w != x or h != y:
    raise "Dimensions collapse"

image = []
threads = []

tree, dmcs, idxs = get_dmc_tree()


bar = ChargingBar('Processed', max = h)

t0 = time.time()

for row in pixels:
    for pixel in row:
        idx = get_thread(pixel, tree)

        thread, rgb = get_thread_info(idx, idxs, dmcs)

        image.append(rgb)
        threads.append(thread)

    bar.next()

print( '\n' + str( time.time() - t0 ) )

image = np.array_split(image, h)
threads = np.array_split(image, h)

visualize(image, address)

os.remove("tmp.jpg")