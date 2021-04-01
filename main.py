import os
import sys
import logging
import logging.handlers
from math import cos, sin, pi, floor
from playable_space import PlayableSpace
from scanner import Scanner
#import adafruit_rplidar

class SyslogBOMFormatter(logging.Formatter):
    def format(self, record):
        result = super().format(record)
        return "\ufeff"+result

handler = logging.handlers.SysLogHandler('/dev/log')
formatter = SyslogBOMFormatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

FIELD_OF_VIEW = 80
CONE_ANGLE = (FIELD_OF_VIEW*2)/3
EXCLUDE_ANGLES = []

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


#Max:   2m
#Close: 1.5m

def react(play, data):
    max_distance = 3000 #3m
    closeTarget = max_distance
    targetCount = 0
    targetAngle = 0
    for angle in range(360):
        if(not(angle in EXCLUDE_ANGLES) and (angle < FIELD_OF_VIEW) or (angle > 360-FIELD_OF_VIEW)):
            distance = data[angle]
            if distance > 0:
                targetCount += 1
                newCloseTarget = min([closeTarget, distance])
                if(newCloseTarget != closeTarget):
                    targetAngle = targetAngle
                    closeTarget = newCloseTarget

    if closeTarget < max_distance:
        right_cone = CONE_ANGLE # CONE_ANGLE to FIELD_OF_VIEW
        left_cone = 360-FIELD_OF_VIEW + CONE_ANGLE #360-FIELD_OF_VIEW to (360-FIELD_OF_VIEW)+CONE_ANGLE
        logging.debug("Targets: "+ str(targetCount))
        print(closeTarget)
        if closeTarget > 100:
            dir = ""
            if(targetAngle > right_cone): #Right zone
                dir = "right"
            elif(targetAngle < left_cone):
                dir = "left"
            else:
                dir = "center"

            if closeTarget < 2000: #mm
                logging.info("Target: ["+ dir + "] " +str(closeTarget))
                if(dir == "left"):
                    play.leftReact()
                elif(dir == "right"):
                    play.rightReact()
                else:
                    play.centerReact()
            #elif closeTarget < 2000:
            #    logging.info("Medium: ["+ dir + "] " + str(closeTarget))
            #    play.mediumReact()
            #elif closeTarget < 2500:
            #    logging.info("Far:   ["+ dir + "] " + str(closeTarget))
            #    play.farReact()
    else:
        logging.debug("Outside bounds: "+str(closeTarget))
        play.off()

#play = PlayableSpace()
scanner = Scanner()
#play.health_check()

event_loop = True

while(event_loop):
    try:
        logging.info(scanner.lidar.info)
        #Use only a tiny buffer to avoid stale data
        for scan in scanner.lidar.iter_scans(max_buf_meas=5,min_len=5):
            scan_data = [0]*360
            for (quality, angle, distance) in scan:
                scan_data[min([359, floor(angle)])] = distance
            fow_data = field_of_view(scan_data)
            react(play, fow_data)
            if VIZ_MODE:
                gui(scan_data)

    except KeyboardInterrupt:
        logging.info('Stopping.')
        event_loop = False
    except:
        logging.exception(sys.exc_info())
        scanner.stop()

scanner.stop()
