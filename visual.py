from PIL import Image
from image_proc import generate_new_name
import numpy as np


def visualize(image, address):
    image = np.array(image, dtype=np.uint8)
    #print(image)

    new_image = Image.fromarray(image)
    new_image.show()
    new_image.save(generate_new_name(address))
