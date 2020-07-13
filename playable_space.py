from time import sleep
from gpiozero import LED

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
