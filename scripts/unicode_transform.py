from __future__ import unicode_literals
from visual import save_image
from PIL import Image, ImageDraw, ImageFont
import numpy as np


h = w = 32
font = ImageFont.truetype(r'..\fonts\ARIALUNI.TTF', size=26)


def transform_unicode(unicode_symb, return_array=False):
    img = Image.new('RGB', (w, h), (255, 255, 255))
    new_img = ImageDraw.Draw(img)

    icon_w, icon_h = new_img.textsize(unicode_symb, font)
    coords = ((w-icon_w) // 2, (h-icon_h) // 2 - 4)
    new_img.text(coords, unicode_symb, fill=(0, 0, 0), font=font)

    img = np.array(img.getdata())
    img = np.reshape(img, (h, w, 3))
    if return_array:
        return img
    if np.all(img == no_symb):
        return
    filepath = '../icons/' + str(ord(unicode_symb)) + '.jpg'
    save_image(img, filepath)


no_symb = transform_unicode(chr(0), return_array=True)


def get_icons(start=0, end=1114111, step=1):
    for i in range(start, end, step):
        transform_unicode(chr(i))


get_icons(start=1000, end=10000)

# ⇔ ▰ ▲ ◐ ◈ ◉ ◤ ▣ ▧
