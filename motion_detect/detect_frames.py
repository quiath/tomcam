# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 22:11:36 2020

@author: quiath

Detect changes in images and move them to permanent storage. 
Delete unchanged images. 

Images are converted to BW and resized to save 
processing power. Able to process over 12 images per second
on Raspberry Pi Zero W.

"""

import sys
from PIL import Image, ImageEnhance, ImageChops
import time
import os
import shutil

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
    pixel_count_thr = 100
    pat = "img%04d.jpg"

    tmpdir = sys.argv[1]
    tgtdir = sys.argv[2]
    i = int(sys.argv[3])
    path = ""

    img1, img2 = None, None
    while True: 
        img1 = img2
        name = pat % i
        oldpath = path
        path = os.path.join(tmpdir, name)
        if not(os.path.isfile(path) and os.path.getsize(path) > 0):
            print("Waiting for", path)
            time.sleep(1)
            continue
        img2 = Image.open(path)
        img2 = resbw(img2)
        if img1 == None:
            i += 1
            continue

        cnt = get_changed_count(img1, img2, thr)
        if cnt > pixel_count_thr:
            print("Copy", path)
            shutil.copy2(path, tgtdir)         
        os.remove(oldpath) 

        i += 1


if __name__ == "__main__":
    main()

