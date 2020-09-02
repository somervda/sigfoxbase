import pycom
import machine
import pytrackHelper
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
from network import WLAN
from machine import I2C
import time

print("Startup")
py = Pytrack()
acc = LIS2HH12()
wlan = WLAN()


# Don't want default blue LED flashes
pycom.heartbeat(False)

# Don't use wifi for my IOT so turn it off to save power
wlan.deinit()
# Turn off accelerometer
py.setup_int_wake_up(True, False)
acc.set_odr(0)

# py.sd_power(False)
pytrackHelper.blink(1, 0x00f0f0)

print("get GPS:", pytrackHelper.getGPS(py, 3))
pytrackHelper.blink(1, 0xff8f00)  # dark orange

print("Sleep..")
# Turn off GPS power
pytrackHelper.blink(1, 0x00ff00)  # Green

py.setup_sleep(10)
py.go_to_sleep(gps=False)
machine.deepsleep(10)
