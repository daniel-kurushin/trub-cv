from math import sin, cos, radians
from matplotlib import pyplot as plt
from time import time
from utilites import load

import numpy as np

x_coordinates = []
y_coordinates = []

x, y, z = 0, 0, 0

out = load('scan-03.json')

def iter_measurments():
    for x in out:
        yield x

def normalize(layer):
    dst = np.zeros(361)
    cnt = np.ones(361)
    zzz = np.zeros(361)
    for z, φ, ρ in layer:
        cnt[round(φ)] += 1
        dst[round(φ)] += ρ
        zzz[round(φ)] = z
    dst /= cnt
    
    rez = []
    for i in range(361):
        rez += [(zzz[i], i, dst[i])]
    
    return rez
        
model = []
layer = []

try:
    φ0 = 0
    for new_scan, quality, φ, ρ in iter_measurments():
        if abs(φ - φ0) > 300:
            model += [normalize(layer)]
            layer = []
        else:
            z += 1
            layer += [(z, φ, ρ)]
        φ0 = φ
    verts = ""
    faces = ""
    n = 0
    for layer in model:
        for angle, dist, z in layer:
            x = dist * cos(radians(angle))
            y = dist * sin(radians(angle))
            verts += "v %s %s %s\n" % (x, y, z)

#    nf = 1
#    for z in range(len(model.keys())-1):
#        for i in range(len(model[z])):
#            a, b = nf,       nf + 1
#            c, d = nf + 361, nf + 360
#            faces += "f %s %s %s %s\n" % (a, b, c, d)
#            nf += 1
    open('/tmp/out.obj','w').write(verts)
#    open('/tmp/out.obj','a').write(faces)        
        
        
except AttributeError:
    pass