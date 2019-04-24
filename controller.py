import time

from joystick import Joystick


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ


def read_controller():
    joystick = Joystick()

    while True:
        start_time = time.time()

        print(joystick.axis_states)
        print(joystick.button_states)

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
