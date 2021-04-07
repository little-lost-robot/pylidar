import adafruit_rplidar
from adafruit_rplidar import RPLidar
from time import sleep
from math import floor
PORT_NAME = '/dev/ttyUSB0'

class Scanner:
    def __init__(self):
        setup = False
        while(not(setup)):
            try:
                self.lidar = RPLidar(None, PORT_NAME)
                self.world_state = [0.0]*360
                setup = True
            except adafruit_rplidar.RPLidarException:
                setup = False

    def fetchScans(self):
        self.lidar.iter_scans()

    def data(self, data):
        scan_data = [0]*360
        for (quality, angle, distance) in data:
            scan_data[min([359, floor(angle)])] = distance
        scan_data

    def fetch360scan(self):
        scans = self.lidar.iter_scans(max_buf_meas=1)
        scan_data = [0]*360
       
        scan = next(scans)
        print(scan)
        for (quality, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance

    def readScan(self):
        scan_samples = self.fetch360scan()
        for idx, distance in enumerate(scan):
            if (abs(distance - world_state[idx]) < 5.0):
                #part of world state
                scan_samples[idx] = 0
        scan_samples

    def stop(self):
        self.lidar.stop()
        self.lidar.disconnect()

    def boot(self):
        print("boot")
        #samples = 4
        #scan_samples = [0]*360
        #for i in range(samples):
        #    sleep(1)
        #    scan_samples[i] = self.fetch360scan()

        #world_state=[0]*360
        #for scan in scan_samples:
        #    for angle in range(360):
        #        distance = scan[angle]
        #        if(distance > 0):
        #            world_data[angle] = distance
        #for idx, total in enumerate(world_state):
        #    world[idx] = total/(samples+0.0)
        #self.world_state = world
        print(self.world_state)

    def debug(self):
        print(self.lidar.info)
        for angle, distance in enumerate(self.world_state):
            print(str(angle) + " -> " + str(distance))
