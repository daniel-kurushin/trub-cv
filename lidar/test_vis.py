from rplidar import RPLidar, RPLidarException
from math import sin, cos, radians
from matplotlib import pyplot as plt
from time import time

TIME_LIMIT = time() + 10

x_coordinates = []
y_coordinates = []

x, y, z = 0, 0, 0

lidar = None
for n in range(0, 4):
    try:
        port = '/dev/ttyUSB%s' % n
        print('Searchin RPLidar on port %s ... ' % port, end = '', flush = 1)
        lidar = RPLidar(port)
        lidar.connect()
        print('done')
        break
    except RPLidarException:
        print('fail!')

def normalize(layer):
    rez = []
    for φ0 in range(360):
        Δφ_min = 360
        out = ()
        for z, φ, ρ in layer:
            Δφ = abs(φ -φ0) 
            if Δφ < Δφ_min:
                out = (z, φ, ρ)
                Δφ_min = Δφ
        rez += [out]
        
model = []
layer = []

try:
    φ0 = 0
    for new_scan, quality, φ, ρ in lidar.iter_measurments():
        if φ < φ0:
            layer = []
            model += [normalize(layer)]
        else:
            z += 0.1
            layer += [(z, φ, ρ)]
        φ0 = φ
        if (time() >= TIME_LIMIT):
            break    
    lidar.disconnect()
    
    verts = ""
    faces = ""
    
    n = 0
    for angle, dist, z in model:
        angle = radians(angle)
        x = dist * cos(angle)
        y = dist * sin(angle)
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