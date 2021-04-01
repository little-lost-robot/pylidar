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
            self.pins[pin] = LED(pin+2)

    def off(self):
        for pin in self.pins:
            pin.off()

    def health_check(self):
        print("health check:")
        for pin in self.pins:
            pin.on()
            sleep(0.1)
            pin.off()
            print(pin)
        print("ok\n")

    def up(self, area):
        self.pins[SOLENOID[area]["up"]].on()

    def down(self, area):
        self.pins[SOLENOID[area]["down"]].off()

    def open(self, area):
        self.pins[SOLENOID[area]["open"]].on()

    def close(self, area):
        self.pins[SOLENOID[area]["close"]].off()

    def responder(self):
        random.choice(list(SOLENOID))

    def leftReact(self):
        self.open("left_canopy_fingers")
        self.up("right_neck")
        sleep(7)

    def rightReact(self):
        self.open("right_canopy_fingers")
        sleep(7)

    def centerReact(self):
        self.open("flowers")
        sleep(7)

    def closeReact(self):
        self.open("left_canopy_fingers")
        self.open("right_canopy_fingers")
        self.open("flowers")
        sleep(7)

    def mediumReact(self):
        self.up("right_neck")
        self.close("flowers")
        sleep(7)

    def farReact(self):
        self.close("right_neck")
        self.close("left_canopy_fingers")
        self.close("right_canopy_fingers")
        if random.randint(0,100) > 80:
            self.open("flowers")
        else:
            self.close("flowers")
        sleep(7)

    def demo(self):
        print("demo...")
        #UP
        self.up("right_neck")
        sleep(12)

        self.open("left_canopy_fingers")
        sleep(8)

        self.open("right_canopy_fingers")
        sleep(8)

        self.open("bench")
        sleep(10)

        self.open("flowers")
        sleep(10)

        #DOWN
        self.close("flowers")
        sleep(10)

        self.close("left_canopy_fingers")
        sleep(10)

        self.close("right_canopy_fingers")
        sleep(10)

        self.close("bench")
        sleep(10)

        self.down("right_neck")
        sleep(18)
        print("done\n")
