import os
from math import cos, sin, pi, floor
import pygame
from playable_space import PlayableSpace
from scanner import Scanner

VIZ_MODE = False
if VIZ_MODE:
    successes, failures = pygame.init()
    print("{0} successes and {1} failures".format(successes, failures))
    screen = pygame.display.set_mode((2000, 1600))
    clock = pygame.time.Clock()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    #Intentional repeat for OSX and pygame *Shrug*
    successes, failures = pygame.init()
    screen = pygame.display.set_mode((2000, 1600))

def gui(data):
    screen.fill((0,0,0))
    for angle in range(360):
        distance = data[angle]
        if distance > 0:
            max_distance = max([min([10, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (1060 + int(x / max_distance * 119), 1020 + int(y / max_distance * 119))
            screen.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()

def react(play, data):
    max_distance = 600
    newTargets = 0.0
    for angle in range(360):
        distance = data[angle]
        if distance > 0:
            newTargets = min([newTargets, distance])

    if newTargets > 0:
        if newTargets < 100:
            play.closeReact()
        elif newTargets < 400:
            play.mediumReact()
        elif newTargets < 600:
            play.farReact()
    else:
        play.off()

play = PlayableSpace()
scanner = Scanner()

play.health_check()
play.demo()

try:
    scanner.boot()
    print(scanner.debug())
    for scan_data in scanner.readScan():
        react(play, scan_data)
        if VIZ_MODE:
            gui(scan_data)

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
