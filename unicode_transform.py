from __future__ import unicode_literals
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.load('arial.pil')

def transform_unicode(unicode_symb):
    img = Image.new('RGB', (17, 17), (255, 255, 255))
    new_img = ImageDraw.Draw(img)
    print(new_img.textsize(unicode_symb, font))
    new_img.text((3, 3), unicode_symb, fill=(0, 0, 0), align='center', font=font)
    img.save('icons/tmp.jpg')

transform_unicode('s')