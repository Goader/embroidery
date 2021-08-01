from PIL import Image
import numpy as np
import os


# Generates special name for the processed image in the form name_edited.jpg
def generate_new_name(filepath):
    return filepath[:filepath.rfind(".")] + "_edited.jpg"


# Generates a filepath to save the created pattern
def generate_pattern_name(filepath):
    prj_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(prj_path, 'patterns', filepath[filepath.rfind("/") + 1:])


# Generates a filepath to save the created mapping
def generate_mapping_name(filepath):
    prj_path = os.path.dirname(os.path.dirname(__file__))
    name = filepath[filepath.rfind("/")+1:].split('.')[0] + '.png'
    return os.path.join(prj_path, 'mappings', name)


def visualize(image, filepath, im_type='image'):
    image = np.array(image, dtype=np.uint8)
    new_image = Image.fromarray(image)
    new_image.show()
    
    if im_type == 'edited':
        new_image.save(generate_new_name(filepath))
    elif im_type == 'pattern':
        new_image.save(generate_pattern_name(filepath))    
    elif im_type == 'mapping':
        new_image.save(generate_mapping_name(filepath))
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
    elif im_type == 'mapping':
        new_image.save(generate_mapping_name(filepath))
    else:
        new_image.save(filepath)
