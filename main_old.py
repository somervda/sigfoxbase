from network import Sigfox
import binascii
import socket
import pycom
import time
import pytrackHelper


def blink(seconds, rgb):
    pycom.rgbled(rgb)
    time.sleep(seconds)
    pycom.rgbled(0x000000)  # off


pycom.heartbeat(False)
blink(1, 0xff8f00)  # dark orange

# init Sigfox for RCZ2 (USA)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ2)

# print Sigfox Device ID
print("SigFox Device ID:", binascii.hexlify(sigfox.id()))

# print Sigfox PAC number
print("Sigfox PAC number:", binascii.hexlify(sigfox.pac()))

print("Sigfox Frequencies:", sigfox.frequencies())

pytrackHelper.getGPS()

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# send some bytes
s.send(bytes([1, 2, 3, 4, 5, 6, 7, 8]))
blink(1, 0x00008b)  # dark blue
