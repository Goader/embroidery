from cv2 import cv2
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
from scipy.fftpack import dct
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import gmpy2
import numpy as np
import time
import os

"""
Transparency

If putting the pixel with RGBA = (Ra, Ga, Ba, Aa) over the pixel with RGBA = (Rb, Gb, Bb, 100%)
we get the output color equal to (Ra*Aa + Rb*(100% - Aa), Ga*Aa + Gb*(100% - Aa), Ba*Aa + Bb*(100% - Aa), 100%)

Tested with Adobe Photoshop :) Works there
"""

GENERATED_PATH = os.path.join('icons', 'generated')


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


def cluster_icons(clusters, hash_size=8):
    img_count = len(os.listdir(GENERATED_PATH))
    assert img_count > clusters, f'There are not enough images in "{GENERATED_PATH}"'

    X = np.zeros((img_count, hash_size * hash_size), dtype=np.uint8)
    names = []
    
    for i, filepath in enumerate(os.listdir(GENERATED_PATH)):
        img = cv2.imread(os.path.join(GENERATED_PATH, filepath))
        names.append(filepath)
        hashed = phash(img)
        X[i, :] = np.array(
            [(hashed >> i) & 1 for i in range(hash_size * hash_size - 1, -1, -1)], 
            np.uint8)

    kmeans = KMeans(n_jobs=-1, n_clusters=clusters)
    X_dist = kmeans.fit_transform(X)

    representative_sign_idx = np.argmin(X_dist, axis=0)

    imgs = []
    for idx in representative_sign_idx:
        read = plt.imread(os.path.join(GENERATED_PATH, names[idx]))
        img = np.zeros((read.shape[0], read.shape[1], 4))

        img[:, :, :3] = read[:, :, :3]
        # add transparency (make PNG out of JPEG)
        if read.shape[-1] == 3:
            img[:, :, 3] = 1.0
        else:
            img[:, :, 3] = read[:, :, 3]

        imgs.append(img)
        
    return imgs


def icon_mapping(threads):
    counter = Counter(map(lambda thr: thr['number'], threads.flatten()))
    clusters = cluster_icons(len(counter))
    
    return {
        number: img for (number, _), img in zip(counter.most_common(), clusters)
    }


def draw_pattern(image, threads):
    icons = icon_mapping(threads)

    factor = 32
    h, w = len(image), len(image[0])
    new_h = h * factor + 2 * ((h * factor - 1) // (10 * factor))
    new_w = w * factor + 2 * ((w * factor - 1) // (10 * factor))

    pattern = np.zeros((new_h, new_w, 3))

    t0 = time.time()
    for y in range(h):
        new_y = y * factor + (y//10) * 2 + 1
        for x, rgb, thread in zip(range(w), image[y], threads[y]):
            new_x = x * factor + (x // 10) * 2 + 1
            
            icon = (np.copy(icons[thread['number']]) * 255).astype(np.uint8)
            dark = not bool(np.mean(rgb[:3]) // 128)

            if dark:
                icon[:, :, :3] = 255 - icon[:, :, :3]

            for y_offset in range(factor - 2):
                for x_offset in range(factor - 2):
                    alpha = icon[y_offset + 1, x_offset + 1, 3] / 255
                    pattern[new_y + y_offset, new_x + x_offset] = (
                        alpha * icon[y_offset + 1, x_offset + 1, :3]
                        + rgb * (1 - alpha))

    print("\nTime spent: ", round(time.time() - t0, 2))
    return pattern, icons


def draw_mapping(icons, threads):
    icons_count = len(icons)

    h_line = 36
    h = icons_count * 36
    w = 300

    prj_path = os.path.dirname(os.path.dirname(__file__))
    font_path = os.path.join(prj_path, 'fonts', 'arial.ttf')
    font = ImageFont.truetype(font_path, size=24)

    img = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    new_img = ImageDraw.Draw(img)

    for i, (number, icon) in enumerate(icons.items()):
        text = f'{number}'

        icon_w, icon_h = new_img.textsize(text, font)
        coords = (50, h_line * i + (h_line-icon_h) // 2)
        new_img.text(coords, text, fill=(0, 0, 0), font=font)


    img = np.array(img)

    def find_rgb(number):
        for thread in threads.flatten():
            if number == thread['number']:
                return thread['rgb']
        raise ValueError(f'No thread with number {number}')

    icon_h, icon_w = 32, 32
    for i, (number, icon_) in enumerate(icons.items()):
        r, g, b = find_rgb(number)
        icon = np.array(Image.new('RGBA', (icon_w, icon_h), (r, g, b, 255)))
        alpha = icon_[:, :, 3:4]

        dark = not bool(np.mean([r, g, b]) // 128)
        if dark:
            icon_[:, :, :3] = 1 - icon_[:, :, :3]

        icon = alpha * 255 * icon_ + (1 - alpha) * icon
        icon = icon.astype(np.uint8)

        coords = (w - 50 - icon_w, h_line * i + (h_line - icon_h) // 2)
        img[coords[1]:coords[1]+icon_h, coords[0]:coords[0]+icon_w, :] = icon

    return img
