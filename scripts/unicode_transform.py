from __future__ import unicode_literals
from visual import save_image
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# font = ImageFont.load(r'C:\Users\Hyperbook\AppData\Local\Microsoft\Windows\Fonts\unifont-13.0.03.pil')
font = ImageFont.truetype(r'fonts\ARIALUNI.TTF', size=26)
# font = ImageFont.truetype(r'C:\Windows\Fonts\Arial\arial.ttf', size=32)

# def post_processing(img):
#     pixels = np.array(img.getdata())
#     for idx, pixel in enumerate(pixels):
#         for c in range(3):
#             pixels[idx][c] = (pixel[c]//128) * 255 

#     pixels[:, :] = (pixels[:, :]//128) * 255 doest it work? this is the question :)

#     pixels = np.reshape(pixels, (img.height, img.width, 3))

#     return pixels

def transform_unicode(unicode_symb):
    h = w = 32
    img = Image.new('RGB', (w, h), (255, 255, 255))
    new_img = ImageDraw.Draw(img)
    icon_w, icon_h = new_img.textsize(unicode_symb, font)
    coords = ((w-icon_w) // 2, (h-icon_h) // 2 - 4)
    new_img.text(coords, unicode_symb, fill=(0, 0, 0), font=font)
    # new_img.bitmap((3, 3), font.getmask(unicode_symb))
    # img.paste(img, mask=font.getmask(unicode_symb))
    # print(font.getmask(unicode_symb))
    # img = post_processing(img)
    img = np.array(img.getdata())
    img = np.reshape(img, (h, w, 3))
    filepath = 'icons/' + str(ord(unicode_symb)) + '.jpg'
    save_image(img, filepath)

transform_unicode('▧')

# ⇔ ▰ ▲ ◐ ◈ ◉ ◤ ▣ ▧