from __future__ import unicode_literals
from visual import save_image
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os


def transform_unicode(unicode_symb, return_array=False, flag=0):
    h = w = 32
    prj_path = os.path.dirname(os.path.dirname(__file__))
    font_path = os.path.join(prj_path, 'fonts', 'ARIALUNI.TTF')
    font = ImageFont.truetype(font_path, size=26)
    if flag != 1:
        no_symb = transform_unicode(chr(0), return_array=True, flag=1)

    img = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    new_img = ImageDraw.Draw(img)

    icon_w, icon_h = new_img.textsize(unicode_symb, font)
    coords = ((w-icon_w) // 2, (h-icon_h) // 2 - 4)
    new_img.text(coords, unicode_symb, fill=(0, 0, 0), font=font)

    img = np.array(img.getdata())
    img = np.reshape(img, (h, w, 4))
    if return_array:
        return img
    if flag != 1 and np.all(img == no_symb):
        return
    filepath = os.path.join(prj_path, 'icons', 'generated', str(ord(unicode_symb)) + '.png')
    save_image(img, filepath)


def get_icons(start=0, end=1114111, step=1):
    for i in range(start, end, step):
        transform_unicode(chr(i))


if __name__ == '__main__':
    get_icons(start=40, end=10000)

# ⇔ ▰ ▲ ◐ ◈ ◉ ◤ ▣ ▧
