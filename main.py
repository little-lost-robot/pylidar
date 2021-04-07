import os
import sys
import logging
import logging.handlers
from math import cos, sin, pi, floor
from playable_space import PlayableSpace
from scanner import Scanner
import adafruit_rplidar

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


FIELD_OF_VIEW = 70
CONE_ANGLE = (FIELD_OF_VIEW*2)/3

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
    max_distance = 3000 #4m
    closeTarget = max_distance
    targetCount = 0
    targetAngle = 0
    for angle in range(360):
        if(angle < FIELD_OF_VIEW or angle > 360-FIELD_OF_VIEW):
            distance = data[angle]
            if distance > 0:
                targetCount += 1 
                newClose = min([closeTarget, distance])
                if(newClose != closeTarget):
                    print("Distance: "+ str(distance))
                    closeTarget = newClose
                    targetAngle = angle
                    

    
    print("Close: "+ str(closeTarget))
    print("Angle: "+ str(targetAngle))
    print("Targets: "+ str(targetCount))
    if closeTarget < max_distance:
        right_cone=CONE_ANGLE
        left_cone = 360-FIELD_OF_VIEW + CONE_ANGLE
        if closeTarget < 1000:
           
            dir = ""
            if(targetAngle > right_cone):
                dir = "left"
                play.leftReact()
            elif(targetAngle < left_cone):
                dir = "right"
                play.rightReact()
            else:
                dir = "center"
                play.centreReact()
            print(dir)

            logging.debug("Targets: "+ str(targetCount))
            print(closeTarget)
            print("Close: "+str(closeTarget))
        else:
            play.off()
    else:
        print("Outside bounds: "+str(closeTarget))
        play.off()

play = PlayableSpace()
scanner = Scanner()
play.health_check()

event_loop = True

while(event_loop):
    try:
        logging.info(scanner.lidar.info)
        #Use only a tiny buffer to avoid stale data
        for scan in scanner.lidar.iter_scans(max_buf_meas=5,min_len=5):
            scan_data = [0]*360
            for (quality, angle, distance) in scan:
                scan_data[min([359, floor(angle)])] = distance
            react(play, scan_data)
            if VIZ_MODE:
                gui(scan_data)

    except KeyboardInterrupt:
        logging.info('Stopping.')
        event_loop = False
    except:
        logging.exception(sys.exc_info())
        scanner.stop()

scanner.stop()
