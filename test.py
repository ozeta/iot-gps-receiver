# import machine
# import math
# import network
# import os
# import utime
# from machine import RTC
# from machine import SD
# from machine import Timer

import gc
import time
from L76GNSS import L76GNSS
from pytrack import Pytrack
from micropyGPS import MicropyGPS

import _thread

time.sleep(1)
gc.enable()

supported_sentences = ('GPRMC', 'GPGGA', 'GPVTG', 'GPGSA', 'GPGSV', 'GPGLL')
location_sentences = ('GPRMC', 'GPGGA', 'GPGLL')
satellite_sentences = ('GPVTG', 'GPGSV')
py = Pytrack()

time.sleep(1)
l76 = L76GNSS(py, timeout=60)
gps = MicropyGPS(location_formatting='dd')


def loop(arg):
    """Loop."""
    # while True:
    for i in range(0, arg):
        # print("i: {}".format(i))
        sentence = l76.raw().decode()
        # print(sentence)
        for x in sentence:
            # if gps.update(x) in location_sentences:
                # if result == 'GPGGA':
            result = gps.update(x)
            if result == 'GNGLL' or result == 'GPGLL':
                print("i: {:10}: ({},{},{}) {} @ {} satellites: {}".format(i, gps.latitude[0], gps.longitude[0], gps.altitude, result, gps.timestamp,gps.satellites_visible()))

        gc.collect()


# loop(10000)
# _thread.start_new_thread(loop, (10000,))
