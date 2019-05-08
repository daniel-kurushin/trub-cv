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


def square(ρ, φ):
    a = ρ
    b = ρ * np.sin(φ)
    return np.sqrt(a**2 + b**2)

def polar_to_cart(ρ, φ, center):
    x = ρ * np.cos(φ) + center[0]
    y = ρ * np.sin(φ) + center[1]
    return int(x), int(y)

def circleToRect(frame):
    w, h = frame.shape[:2]
    c    = (w//2, h//2)
    rez = np.zeros([w,h])
    ρ = w // 2
    for x in range(w):
        for y in range(h):
            φ = np.arctan((y - c[0])/(x - c[1])) if x - c[1] != 0 else np.radians(90)
            nx, ny = polar_to_cart(ρ, φ, c)
            try:
                rez[w-x-1,y] = frame[nx, ny]
            except IndexError:
                print(x, y, nx, ny)
                break
        ρ -= 1
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


#    for ρ in np.linspace(start = 0, stop = w/2, num = w-1):
#        for φ in np.linspace(start = 0, stop = np.radians(360), num = h-1):
#            nx, ny = polar_to_cart(ρ, φ, (w/2, h/2))
#            x, y = polar_to_cart(square(ρ, φ), φ, (w/2, h/2))
##            print(x, y, ρ, φ, nx, ny)
#            try:
#                rez[x,y] = frame[nx, ny]
##                print(round(ρ,2), round(φ, 2), x, y, nx, ny)
##                break
#            except IndexError:
#                print(x,y,nx,ny)
#                pass
#                
#            x += 1
#        y += 1
