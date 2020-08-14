from time import sleep
from gpiozero import LED

SOLENOID = {
    "right_neck":     {"up":   1, "down": 2},
    "canopy_fingers": {"open": 3, "close": 4},
    "canopy_center":  {"open": 5, "close": 6},
    "flowers":        {"open": 8, "close": 7},
    "bench":          {}
}

class PlayableSpace:
    def __init__(self):
        self.pings = []
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

    def demo(self):
        #UP
        up("right_neck")
        sleep(1000 * 12)
        open("canopy_fingers")
        sleep(1000 * 8)

        open("canopy_center")
        sleep(1000 * 12)

        open("flowers")
        sleep(1000 * 10)

        #DOWN
        close("flowers")
        sleep(1000 * 10)
        close("canopy_center")
        sleep(1000 * 18)
        close("canopy_fingers")
        sleep(1000 * 18)
        down("right_neck")
        sleep(1000 * 18)
