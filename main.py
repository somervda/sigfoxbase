import pycom
import machine
import pytrackHelper
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
from network import WLAN
from network import Sigfox
import socket
import binascii
from machine import I2C
import time
import struct

print("Startup")
py = Pytrack()
acc = LIS2HH12()
wlan = WLAN()

py = Pytrack()


# Don't want default blue LED flashes
pycom.heartbeat(False)

# Don't use wifi for my IOT so turn it off to save power
wlan.deinit()
# Turn off accelerometer
py.setup_int_wake_up(True, False)
acc.set_odr(0)

pytrackHelper.blink(2, 0xff8f00)  # dark orange

# init Sigfox for RCZ2 (USA)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ2)

# print Sigfox Device ID
print("SigFox Device ID:", binascii.hexlify(sigfox.id()))

# print Sigfox PAC number
print("Sigfox PAC number:", binascii.hexlify(sigfox.pac()))

print("Sigfox Frequencies:", sigfox.frequencies())

gps_data = pytrackHelper.getGPS(py, 300)
longitude = gps_data[0]
latitude = gps_data[1]

if longitude is None or latitude is None:
    longitude = 0.0
    latitude = 0.0

print("get GPS:", gps_data)
data_packed = struct.pack("ff", longitude, latitude)
print("GPS packed:", data_packed)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# send some bytes
s.send(data_packed)
print("Sleep..")
# Turn off pytrack
pytrackHelper.blink(1, 0x00ff00)  # Green

py.setup_sleep(600)
py.go_to_sleep(gps=False)
# machine.deepsleep(10)
