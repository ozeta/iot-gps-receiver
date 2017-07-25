import socket
import network
import time
import pycom
import _thread
from pytrack import Pytrack
from L76GNSS import L76GNSS
from timer import Timer as Timer
PORT = 54500
HOST = '0.0.0.0'
CONTENT = '(10.10,20.20)'
counter = 0

py = Pytrack()
l76 = L76GNSS(py, timeout=120)
coords = (1, 1)
coord_lock = _thread.allocate_lock()
loop_guard = True
print("lan: ", wl.ifconfig())

def get_coord():
    """Get coords."""
    interval = 1000
    times = Timer()
    while True:
        times.start()
        with coord_lock:
            coords = l76.coordinates()
            print(coords)
        lap = times.stop()
        if lap < interval:
            time.sleep_ms(interval - lap)
    return


def start():
    """AAAH ."""
    while True:
        c = None
        s = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((HOST, PORT))
            s.listen(1)
            print("Socket Server is : 'Listening' ")
            c, addr = s.accept()
            print('Accepted connection from ', addr)
            while True:
                pycom.rgbled(0x002222)
                with coord_lock:
                    packet = "{}".format(coords)
                    time.sleep(2)
                pycom.rgbled(0x00ffff)
                c.send(packet)
            print("connection ended")
        finally:
            if c is not None:
                c.close()
            if s is not None:
                s.close()
            pycom.heartbeat(True)


# _thread.start_new_thread(get_coord, ())
# _thread.start_new_thread(start, ())
