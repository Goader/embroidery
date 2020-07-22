from PIL import Image
from image_proc import generate_new_name, generate_scheme_name
import numpy as np


def visualize(image, filepath, im_type='i'):
    image = np.array(image, dtype=np.uint8)
    new_image = Image.fromarray(image)
    new_image.show()
    new_image.save(generate_new_name(filepath) if im_type == 'i' else generate_scheme_name(filepath))


def show_image(image):
    image = np.array(image, dtype=np.uint8)
    new_image = Image.fromarray(image)
    new_image.show()


def save_image(image, filepath, im_type='i'):
    image = np.array(image, dtype=np.uint8)
    new_image = Image.fromarray(image)
    new_image.save(generate_new_name(filepath) if im_type == 'i' else generate_scheme_name(filepath))
