from tkinter import *
from serial import Serial, SerialException
from math import radians, sin, cos

arduino = None
for n in range(4):
    try:
        arduino = Serial(port='/dev/ttyUSB%s' % n, baudrate=9600)
        break
    except SerialException:
        pass
root = Tk()

c = Canvas(root, width=800, height=800, bg='white')

points = [0] * 360
dists = [100] * 360
model = {}

x, y, z = 0, 0, 0

verts = ""

def saveObjFile():
    verts = ""
    faces = ""
    for z in range(len(model.keys())):
        for i in range(len(model[z])):
            dist = model[z][i]
            angle = radians(i)
            x = dist * cos(angle)
            y = dist * sin(angle)
            verts += "v %s %s %s\n" % (x, y, z + i / 360)

    nf = 1
    for z in range(len(model.keys())-1):
        for i in range(len(model[z])):
            a, b = nf,       nf + 1
            c, d = nf + 361, nf + 360
            faces += "f %s %s %s %s\n" % (a, b, c, d)
            nf += 1
    open('/tmp/out.obj','w').write(verts)
    open('/tmp/out.obj','a').write(faces)
    
def initPoints():
    dist = 100
    for i in range(360):
        angle = radians(i)    
        x = 400 + dist * cos(angle)
        y = 400 - dist * sin(angle)
        x1, y1 = (x - 1), (y - 1)
        x2, y2 = (x + 1), (y + 1)
        points[i] = c.create_oval(x1, y1, x2, y2, fill="#476042")
        
adist, sdist = 0, 100

def getPoint():
    global x, y, z, adist, sdist
    try:
        i, dist = [ int(x) for x in arduino.readline().strip(b'\n').split() ]
        sdist = sdist + dist - adist
        adist = sdist / 10
        angle = radians(i)
        x = 400 + adist * cos(angle)
        y = 400 - adist * sin(angle)
        dists[i] = adist
        if angle == 0:
            model.update({z:dists[:]})
            if z > 19:
                root.after(1, winClose)
            else:
                z += 1

        x1, y1 = (x - 1), (y - 1)
        x2, y2 = (x + 1), (y + 1)
        c.coords(points[i], x1, y1, x2, y2)
    except ValueError:
        pass
    
    root.after(10, getPoint)
    
def winClose():
    root.destroy()
    saveObjFile()

root.after(   10, initPoints)
root.after(   20, getPoint)

c.pack()
root.mainloop()

