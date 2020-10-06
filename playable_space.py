from time import sleep
from gpiozero import LED
import random

SOLENOID = {
    "right_neck":           {"up":   1, "down": 2,    "open": 1, "close": 2},
    "left_canopy_fingers":  {"open": 13, "close": 14},
    "right_canopy_fingers": {"open": 15, "close": 16},
    "flowers":              {"open": 11, "close": 12},
    "bench":                {"open": 9, "close": 10}
    #"spare1":               {"open": 3, "close": 4},
    #"spare2":               {"open": 5, "close": 6},
    #"spare3":               {"open": 7, "close": 8},
}

class PlayableSpace:
    def __init__(self):
        self.pins = [0]*20
        for pin in range(20):
            self.pins[0] = LED(pin+2)

    def off(self):
        for pin in self.pins:
            pin.off()

    def health_check(self):
        for pin in self.pins:
            pin.on()
            sleep(1000)
            pin.off()
            sleep(1000)

    def up(self, area):
        pins[SOLENOID[area]["up"]].on()

    def down(self, area):
        pins[SOLENOID[area]["down"]].off()

    def open(self, area):
        pins[SOLENOID[area]["open"]].on()

    def close(self, area):
        pins[SOLENOID[area]["close"]].off()

    def responder(self):
        random.choice(list(SOLENOID))

    def closeReact(self):
        open("left_canopy_fingers")
        open("right_canopy_fingers")
        open("flowers")
        sleep(1000 * 8)

    def mediumReact(self):
        up("right_neck")
        sleep(1000 * 12)
        close("flowers")
        sleep(1000 * 8)

    def farReact(self):
        close("right_neck")
        close("left_canopy_fingers")
        close("right_canopy_fingers")
        if random.randint(0,100) > 80:
            open("flowers")
        else:
            close("flowers")
        sleep(1000 * 10)

    def demo(self):
        #UP
        up("right_neck")
        sleep(1000 * 12)

        open("left_canopy_fingers")
        sleep(1000 * 8)

        open("right_canopy_fingers")
        sleep(1000 * 8)

        open("bench")
        sleep(1000 * 10)

        open("flowers")
        sleep(1000 * 10)

        #DOWN
        close("flowers")
        sleep(1000 * 10)

        close("left_canopy_fingers")
        sleep(1000 * 10)

        close("right_canopy_fingers")
        sleep(1000 * 10)

        close("bench")
        sleep(1000 * 10)

        down("right_neck")
        sleep(1000 * 18)
