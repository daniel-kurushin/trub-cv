from rplidar import RPLidar, RPLidarException
from time import time
from datetime import datetime
from utilites import dump
from os.path import isfile

FNAME = '/tmp/out.%s.json'
LOCK = '/tmp/lock'

def now():
    return str(datetime.now())

def connect_to_lidar():
    lidar = None
    for n in range(0, 4):
        try:
            port = '/dev/ttyUSB%s' % n
            print('Searchin RPLidar on port %s ... ' % port, end = '', flush = 1)
            lidar = RPLidar(port)
            lidar.connect()
            print('done')
            return lidar
            
        except RPLidarException:
            print('fail!')

def start_recording(lidar, fname):
    try:
        open(LOCK, 'w').write(now())
        out = []
        for new_scan, quality, φ, ρ in lidar.iter_measurments():
            out += [(time(), new_scan, quality, φ, ρ)]
            if len(out) > 100000:
                dump(object=out, filename=fname % now())
                out = []
                if not isfile(LOCK):
                    break
    except Exception as e:
        raise e

if __name__ == '__main__':
    lidar = connect_to_lidar()
    start_recording(lidar, FNAME)