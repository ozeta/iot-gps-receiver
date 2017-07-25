import time
import _thread
from timer import Timer as Timer

counter = 0
coord_lock = _thread.allocate_lock()
coords = list()


def producer(interval):
    tim = counter
    for i in range(interval):
        with coord_lock:
            dic = (tim, tim)
            print(dic)
            coords.append(dic)
            time.sleep(1)
        tim += 1


def consumer(interval):
    for i in range(interval):
        with coord_lock:
            print(coords)
            time.sleep(2)


_thread.start_new_thread(producer, (5,))
_thread.start_new_thread(consumer, (5,))
