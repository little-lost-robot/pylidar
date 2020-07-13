"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import pygame
from adafruit_rplidar import RPLidar
from gpiozero import LED

import os
from math import cos, sin, pi, floor

from playable_space import PlayableSpace

play = PlayableSpace()

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((2000, 1600))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).

rect = pygame.Rect((0, 0), (32, 32))
image = pygame.Surface((32, 32))
image.fill(WHITE)

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((2000, 1600))
#pygame.mouse.set_visible(False)

PORT_NAME = '/dev/ttyUSB0'
PORT_NAME = '/dev/tty.SLAB_USBtoUART'
lidar = RPLidar(None, PORT_NAME)

# used to scale data to fit on the screen
max_distance = 600

#pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    screen.fill((0,0,0))
    for angle in range(360):
        distance = data[angle]
        if distance > 0:   # ignore initially ungathered data points
            max_distance = max([min([10, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (1060 + int(x / max_distance * 119), 1020 + int(y / max_distance * 119))
            screen.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()


scan_data = [0]*360

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
