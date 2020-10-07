import os
import sys
from math import cos, sin, pi, floor
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
    max_distance = 4000 #4m
    closeTarget = max_distance 
    for angle in range(360):
        distance = data[angle]
        if distance > 0:
            closeTarget = min([closeTarget, distance])

    if closeTarget < max_distance:
        print(closeTarget)
        if closeTarget < 500:
            print("close")
            #play.closeReact()
        elif closeTarget < 1500:
            print("medium")
            #play.mediumReact()
        elif closeTarget < 3500:
            print("far")
            #play.farReact()
    else:
        print()
        #play.off()

play = PlayableSpace()
scanner = Scanner()
play.health_check()

try:
    print(scanner.lidar.info)
    #Use only a tiny buffer to avoid stale data
    for scan in scanner.lidar.iter_scans(max_buf_meas=1,min_len=5):
        scan_data = [0]*360
        for (quality, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        react(play, scan_data)
        if VIZ_MODE:
            gui(scan_data)

except KeyboardInterrupt:
    print('Stoping.')
#except:
#    print(sys.exc_info()[0])

scanner.stop()
