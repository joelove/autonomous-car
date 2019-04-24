import time

from joystick import Joystick
from threading import Thread
from multiprocessing import Pipe


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ


def read_controller():
    joystick = Joystick()
    joystick.init()

    parent_connection, child_connection = Pipe()

    thread = Thread(target=joystick.begin_polling, args=(child_connection,))
    thread.daemon = True
    thread.start()

    while True:
        start_time = time.time()

        axis_states = parent_connection.recv()
        print(axis_states)

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
