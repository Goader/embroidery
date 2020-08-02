from cv2 import cv2
import numpy as np
import time

"""
Transparency

If putting the pixel with RGBA = (Ra, Ga, Ba, Aa) over the pixel with RGBA = (Rb, Gb, Bb, 100%)
we get the output color equal to (Ra*Aa + Rb*(100% - Aa), Ga*Aa + Gb*(100% - Aa), Ba*Aa + Bb*(100% - Aa), 100%)

Tested with Adobe Photoshop :) Works there
"""
def draw_pattern(image, threads):
    factor = 32
    h, w = len(image), len(image[0])
    new_h = h * factor + 2 * ((h * factor - 1) // (10 * factor))
    new_w = w * factor + 2 * ((w * factor - 1) // (10 * factor))

    pattern = np.zeros((new_h, new_w, 3))
    threads = np.transpose(threads)

    t0 = time.time()
    for y in range(h):
        new_y = y * factor + (y//10) * 2 + 1
        for x, rgb, thread in zip(range(w), image[y], threads[y]):
            # icon = cv2.imread(thread['icon'], -1)
            icon = cv2.imread('icons/9639.png', -1)

            new_x = x * factor + (x // 10) * 2 + 1

            for y_offset in range(factor - 2):
                for x_offset in range(factor - 2):
                    alpha = int(icon[y_offset + 1, x_offset + 1, 3]) / 255
                    pattern[new_y + y_offset, new_x + x_offset] = (
                        alpha * icon[y_offset + 1, x_offset + 1, :3]
                        + rgb * (1 - alpha))

    print("\nTime spent: ", round(time.time() - t0, 2))
    return pattern
