#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 21:11:25 2019

@author: dan
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from roundrect import roundrect

n = 1
for f in ['data/01.mp4', 'data/02.mp4', 'data/03.mp4', 'data/04.mp4']:
    cap = cv.VideoCapture(f)
    ret,frame = cap.read()
    frame_cr = roundrect(cv.cvtColor(frame, cv.COLOR_BGR2GRAY))# frame_cr = frame[450:2550, 450:2550]
    
    cv.imwrite('data/r_%s.jpeg' % n, frame_cr)
    n += 1




#frame1 = roundrect(frame1)
#plt.imshow(frame1, 'gray')
#plt.show()
## frame2 = roundrect(frame2)
#plt.imshow(frame2, 'gray')
#plt.show()

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
