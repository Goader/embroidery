from PIL import Image
from image_proc import generate_new_name, generate_pattern_name
import numpy as np


def visualize(image, filepath, im_type='image'):
    image = np.array(image, dtype=np.uint8)
    new_image = Image.fromarray(image)
    new_image.show()
    
    if im_type == 'edited':
        new_image.save(generate_new_name(filepath))
    elif im_type == 'pattern':
        new_image.save(generate_pattern_name(filepath))
    else:
        new_image.save(filepath)


def show_image(image):
    image = np.array(image, dtype=np.uint8)
    new_image = Image.fromarray(image)
    new_image.show()


def save_image(image, filepath, im_type='image'):
    image = np.array(image, dtype=np.uint8)
    new_image = Image.fromarray(image)
    
    if im_type == 'edited':
        new_image.save(generate_new_name(filepath))
    elif im_type == 'pattern':
        new_image.save(generate_pattern_name(filepath))
    else:
        new_image.save(filepath)