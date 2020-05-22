import cv2 as cv
import re
import numpy as np
import matplotlib.pyplot as plt
from json import load

from glob import glob

points = load(open('/tmp/ppp','r'))

bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
orb = cv.ORB_create()
des0 = []
x0, y0 = 250, 250
xx, yy = 250, 250
measured_points = []

for fname in sorted(glob('../data/geo-scan-*'), key = lambda x : int(re.search('\d+', x).group())):
    kp1, des1 = orb.detectAndCompute(cv.imread(fname,cv.IMREAD_GRAYSCALE),None)
    matches = sorted(bf.match(des1,des0), key = lambda x:x.distance)
    dx = np.mean([ kp1[match.trainIdx].pt[0] - kp1[match.queryIdx].pt[0] for match in matches ])
    dy = np.mean([ kp1[match.trainIdx].pt[1] - kp1[match.queryIdx].pt[1] for match in matches ])
    
    if np.isnan(dx) and np.isnan(dy):
        dx, dy = 0, 0
    measured_points += [(xx,yy)]
    xx += dx 
    yy += dy
    kp0, des0 = kp1, des1
    
plt.plot([ x for x,y in measured_points ], [ y for x,y in measured_points ])
plt.plot([ x for x,y in points ], [ y for x,y in points ])
plt.show()