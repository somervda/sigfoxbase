import pycom
import machine
import pytrackHelper
from pytrack import Pytrack
import time


def blink(seconds, rgb):
    pycom.rgbled(rgb)
    time.sleep(seconds)
    pycom.rgbled(0x000000)  # off


print("hello")
# Don't want default blue LED flashes
pycom.heartbeat(False)
# Don't use wifi for my IOT so turn it off to save power
pycom.wifi_on_boot(False)
# Turn off and on things I'm using on the pytracker
py = Pytrack()
# py.sd_power(False)
py.gps_state(True)
blink(1, 0x00f0f0)

print("get GPS:", pytrackHelper.getGPS(py, 120))
blink(1, 0xff8f00)  # dark orange

print("Sleep..")
# Turn off GPS power
# py.go_to_sleep(gps=False)
py.gps_state(False)
blink(1, 0x00ff00)  # Green
machine.deepsleep(30000)
