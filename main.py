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

import os
from math import cos, sin, pi, floor
import pygame
from playable_space import PlayableSpace

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
screen = pygame.display.set_mode((2000, 1600))
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Intentional repeat for OSX and pygame *Shrug*
successes, failures = pygame.init()
screen = pygame.display.set_mode((2000, 1600))

play = PlayableSpace()
scanner = Scanner()

play.health_check()

def process_data(data):
    max_distance = 600
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

try:
    scanner.boot()
    print(scanner.debug())
    for scan_data in scanner.fetch360scan():
        process_data(scan_data)

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
