from network import Sigfox
import socket
import binascii

#  See https://docs.pycom.io/tutorials/networks/sigfox/


# ***** Initialize Sigfox for USA - RCZ2 and print out Sigfox info
class SIGFOXHELPER:

    def __init__(self):
        self.sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ2)

    def info(self):
        # print Sigfox Device ID
        print("SigFox Device ID:", binascii.hexlify(self.sigfox.id()))
        # print Sigfox PAC number
        print("Sigfox PAC number:", binascii.hexlify(self.sigfox.pac()))
        print("Sigfox Frequencies:", self.sigfox.frequencies())

    def send(self, payload):
        # create a Sigfox socket
        s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
        # make the socket blocking
        s.setblocking(True)
        # configure it as uplink only
        s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
        # send gps_data with Sigfox
        s.send(payload)
