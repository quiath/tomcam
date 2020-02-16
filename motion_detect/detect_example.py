# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 22:11:36 2020

@author: quiath

Simple example how to detect changes between images
that were sequentially written to disk.

Images are converted to BW and resized to save 
processing power. Able to process over 12 images per second
on Raspberry Pi Zero W.

"""

import sys
from PIL import Image, ImageEnhance, ImageChops

W, H = 160, 120

def resbw(img):
    return img.convert(mode="L").resize((W, H), resample=Image.NEAREST)

def get_changed_count(img1, img2, threshold):
    img = ImageChops.difference(img1, img2)
    cplist = img.getcolors(256)
    notchanged = sum(x[0] for x in cplist if x[1] < threshold)
    return img.size[0] * img.size[1] - notchanged


def main():
    thr = 20
    pat = "half%03d.jpg"
    img1, img2 = None, None
    for i in range(1, 1000):
        img1 = img2
        img2 = Image.open(pat % i)
        img2 = resbw(img2)
        if img1 == None:
            continue

        cnt = get_changed_count(img1, img2, thr)

        print(i - 1, i, cnt)


if __name__ == "__main__":
    main()

