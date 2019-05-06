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
    def rect_to_circle(a,b):
        a = a - w//2
        b = b - h//2
        r = a
        f = a / b
        return a, b
    
    w, h = frame.shape[:2]
    rez = np.zeros([w,h])
    for x in range(w):
        for y in range(h):
            nx, ny = rect_to_circle(x, y)
            rez[x,y] = frame[nx, ny]
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
