#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:30:43 2019

@author: dan
"""

import numpy as np
import cv2 as cv



def roundrect(img):

    def polar_to_cart(ρ, φ, center):
        x = ρ * np.cos(φ) + center[0]
        y = ρ * np.sin(φ) + center[1]
        return int(x), int(y)

    h, w = img.shape[:2]
    c = w//2, h//2
    out = np.ones([w,h]) * 255
    
    for x in range(w):
        for y in range(h):
            φ = np.radians(0) + np.arctan((x - c[0])/(y - c[1])) if y - c[1] != 0 else np.radians(90)
            ρ = max(abs(x-c[0]),abs(y-c[1])) if y > h // 2 else -max(abs(x-c[0]),abs(y-c[1]))
            nx, ny = polar_to_cart(ρ, φ, c)
            out[y, x] = img[nx,ny]
            
    return out


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    
    for i in [0,1,2,3,4]:
        img1 = cv.cvtColor(cv.imread('in%s.png' % i), cv.COLOR_BGR2GRAY)

        plt.imshow(img1, 'gray', vmax = 255, vmin = 0)
        plt.show()

        img2 = roundrect(img1)
        plt.imshow(img2, 'gray', vmax = 255, vmin = 0)
        plt.show()

