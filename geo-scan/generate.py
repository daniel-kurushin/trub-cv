import cv2 as cv
from random import randint
from json import dump

src_img = cv.imread('../data/geo-scan.png')

x = 0

w, h = 500, 500
points = []
for i in range(50):
    x += randint(1,3)
    y = randint(1,3)
    frame = src_img[y:y+h, x:x+w]
    cv.imwrite('../data/geo-scan-%s.png' % i, frame)
    points += [(250 + x, 250 + y)]
    
dump(points, open('/tmp/ppp','w'))