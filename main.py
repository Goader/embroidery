from src.image_proc import get_image, resize_image, process_image
from src.pattern import draw_pattern
from scripts.visual import visualize, save_image
import numpy as np
import os

"""
Embroidery patterns

This program is created to generate embroidery patterns been given only
the input image and the size of the embroidery picture.

It uses special algorithms to find the most appropriate DMC thread for a
particular color represented as RGB tuple. Involves using Floyd Steinberg's
algorithm for better effect and to make the output image smoother for the
human eye. ...

Based on the selected threads, generates all the needed documentation for
an ordinary person to start embroidering. 

Specific scripts for generating .json file of DMC threads, creating icons
for a pattern from Unicode symbols, selecting most dissimilar ones provided.
"""


if __name__ == "__main__":
    try:
        address = input("Input image file path: ")
        x = int(input("Type in width:  "))
        y = int(input("Type in height: "))

        # Resizing the given image to the provided size above
        new_address = resize_image(address, x, y)

        pixels, size = get_image(new_address)
        pixels = np.array(pixels)
        pixels = pixels.transpose((1, 0, 2))
        w, h = size

        if w != x or h != y:
            raise Exception("Dimensions collapse")

        # Selecting existing threads for every pixel
        image, threads = process_image(pixels, w, h)

        # visualize(image, address, im_type='edited')
        save_image(image, address, im_type='edited')

        os.remove("tmp.jpg")

        # Generating the pattern based on the selected threads
        pattern = draw_pattern(image, threads)

        visualize(pattern, address, im_type='pattern')
    
    except KeyboardInterrupt:
        if os.path.exists("tmp.jpg"):
            os.remove("tmp.jpg")
        exit()

