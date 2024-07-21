import time
from machine import Pin
import _thread

    
class Lighter:
    def __init__(self, pin_num=2):
        self.light = Pin(pin_num, Pin.OUT)
        self.blinking = False

    def blink(self, interval=1):
        self.blinking = True
        _thread.start_new_thread(self.__internal_blink, (interval,))
    
    def close(self):
        self.blinking = False
        self.light.value(False)
    
    def __internal_blink(self, interval):
        while self.blinking:
            self.light.value(not self.light.value())
            time.sleep(interval)


if __name__ == '__main__':
    light = Lighter(2)
    light.blink(0.3)
    time.sleep(5)
    light.close()
    print('done ---')

