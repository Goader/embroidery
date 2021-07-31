from scipy.fftpack import dct
from cv2 import cv2
from visual import save_image
from PIL import Image
import gmpy2
import os
import numpy as np


def eucl_dist(img1, img2):
    delta = img1 - img2
    return np.sum(np.square(delta))


def phash(img, hash_size=8, factor=4):
    img = np.array(img, dtype=np.uint8)
    img = Image.fromarray(img)
    image_size = hash_size * factor
    img.convert('L').resize((image_size, image_size), Image.ANTIALIAS)
    img = np.asarray(img)[:, :, 0]
    dct_ = dct(dct(img, axis=0), axis=1)
    dct_ = dct_[:hash_size, :hash_size]
    med = np.median(dct_)
    diff = dct_ > med
    return sum((1 << i) * int(el) for i, el in enumerate(diff.flatten()))


# FIXME doesn't work!! vv
if __name__ == '__main__':
    icons = []
    imgs = []
    for filename in os.listdir('../icons/generated/'):
        if filename.endswith('.jpg'):
            imgs.append(np.array(cv2.imread('../icons/generated/' + filename)))

    for idx, filename in enumerate(os.listdir('../icons/generated/')):
        if filename.endswith('.jpg'):
            # distance = sum(eucl_dist(imgs[idx], other_img) for other_img in imgs)
            distance = 0

            icons.append({'filename': filename,
                          'ord': filename[:filename.rfind('.')],
                          'distance': distance,
                          'image': imgs[idx],
                          'phash': phash(imgs[idx])})

    for icon1 in icons:
        distance = 0
        for icon2 in icons:
            distance += gmpy2.popcount(int(np.bitwise_xor(icon1['phash'], icon2['phash'])))
        icon1['distance'] = distance

    icons.sort(key=lambda x: x['distance'])
    icons = icons[::-1]

    for i, icon in enumerate(icons, 1000):
        save_image(icon['image'], f'../icons/clustered/_{i}_{icon["ord"]}.jpg')
