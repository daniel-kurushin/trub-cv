#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:30:43 2019

@author: dan
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def square(ρ, φ):
    a = ρ
    b = ρ * np.sin(φ)
    return np.sqrt(a**2 + b**2)

def polar_to_cart(ρ, φ, center):
    x = ρ * np.cos(φ) + center[0]
    y = ρ * np.sin(φ) + center[1]
    return int(x), int(y)

img1 = cv.imread('in.png')
img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
plt.imshow(img1, vmax = 255, vmin = 0)
plt.show()
h, w = img1.shape[:2]
c = w//2, h//2

img2 = np.zeros([w,h])*255
ρ = 9
for x in range(w):
    for y in [0]:
        φ = np.arctan((y - c[0])/(x - c[1])) if x - c[1] != 0 else np.radians(90)
        nx, ny = polar_to_cart(ρ, φ, c)
        try:
            img2[y,x] = img1[ny,nx]
        except IndexError:
            print(nx, ny)


plt.imshow(img2, vmax = 255, vmin = 0)
plt.show()
