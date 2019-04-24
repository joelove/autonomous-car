import time

from joystick import Joystick
from multiprocessing import Process, Pipe


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ


def read_controller():
    parent_connection, child_connection = Pipe()

    joystick = Joystick()
    joystick.init()

    process = Process(target=joystick.begin_polling, args=(child_connection,))
    process.start()

    while True:
        start_time = time.time()

        axis_states = parent_connection.recv()

        print(axis_states)

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
