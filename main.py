import pycom
import machine
from machine import I2C
import pytrackHelper
from pytrackHelper import GPS_Payload
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
from network import WLAN
from sigfoxHelper import SIGFOXHELPER
import time

# Setup , turn off heartbeat LED and create required objects
pycom.heartbeat(False)
print("Startup")
py = Pytrack()
acc = LIS2HH12()
wlan = WLAN()
sfh = SIGFOXHELPER()
sfh.info()

# Don't use wifi so turn it off to save power
wlan.deinit()
# Turn off accelerometer
py.setup_int_wake_up(True, False)
acc.set_odr(0)

#  Get the GPS Data
pytrackHelper.blink(2, 0xff8f00)  # dark orange
gps = pytrackHelper.getGPS(py, 300)
gps_payload = GPS_Payload(gps[0], gps[1])
print("GPS packed: {} Size {}".format(
    gps_payload.pack(), gps_payload.calcsize()))

# Send data via sigfox
sfh.send(gps_payload.pack())

# Turn off pytrack to minimize power
pytrackHelper.blink(1, 0x00ff00)  # Green
py.setup_sleep(600)
print("Sleep..")
py.go_to_sleep(gps=False)
# machine.deepsleep(10)
