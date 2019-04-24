import time

from joystick import Joystick


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ


def read_controller():
    joystick = Joystick()

    joystick.init()

    while True:
        start_time = time.time()

        button, button_state, axis, axis_val = joystick.poll()
        print(axis, axis_val)

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
