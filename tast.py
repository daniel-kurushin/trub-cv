#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 21:11:25 2019

@author: dan
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

cap1 = cv.VideoCapture('data/03.mp4')
cap2 = cv.VideoCapture('data/02.mp4')

ret,frame1 = cap1.read()
ret,frame2 = cap2.read()

frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)

height, width = frame1.shape[:2]
frame1 = cv.resize(frame1,(width // 10, height // 10), interpolation = cv.INTER_CUBIC)

def circleToRect(frame):
    def polar_to_cart(ρ, φ, center):
        x = ρ  * np.cos(φ) + center[0]
        y = ρ  * np.cos(φ) + center[1]
        return int(x), int(y)
    
    w, h = frame.shape[:2]
    rez = np.zeros([w,h])
    y = 0
    for ρ in np.linspace(start = 0, stop = w/2, num = w-1):
        x = 0
        for φ in np.linspace(start = 0, stop = np.radians(180), num = h-1):
            nx, ny = polar_to_cart(x, y, (w/2, h/2))
#            print(x, y, ρ, φ, nx, ny)
            try:
                rez[y,x] = frame[nx, ny]
                print(x, y, nx, ny)
                break
            except IndexError:
                pass
            x += 1
        y += 1
    return rez

plt.imshow(frame1, 'gray')
plt.show()
frame1 = circleToRect(frame1)
plt.imshow(frame1, 'gray')
plt.show()

#cv.waitKey(300)
#cv.imshow('frame',frame2)
#cv.waitKey(30)


#frame2 = cv.resize(frame2,(width // 10, height // 10), interpolation = cv.INTER_CUBIC)
#plt.imshow(frame2, 'gray')
#plt.show()
