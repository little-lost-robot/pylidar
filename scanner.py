from adafruit_rplidar import RPLidar
PORT_NAME = '/dev/ttyUSB0'
PORT_NAME = '/dev/tty.SLAB_USBtoUART'

class Scanner:
    def __init__(self):
        self.lidar = RPLidar(None, PORT_NAME)
        self.world_state = [0.0]*360

    def fetch360scan(self):
        scan = self.lidar.iter_scans()
        scan_data = [0]*360
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance

    def boot(self):
        samples = 4
        scan_samples = []
        for i in range(samples):
            sleep(1000)
            scan_samples[i] = fetch360scan

        world_state=[0]*360
        for scan in scan_samples:
            for angle in range(360):
                distance = data[angle]
                if(distance > 0):
                    world_data[angle] = distance
        for idx, total in enumerate(world_state):
            world[idx] = total/samples
        self.wordl_state = world

    def debug(self):
        self.lidar.info
        for angle, distance in enumerate(self.world_state):
            println(angle + " -> " + distance)
