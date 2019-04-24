import time

from joystick import Joystick


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ


def read_controller():
    joystick = Joystick()

    joystick.init()

    result = joystick.begin_polling()

    while True:
        start_time = time.time()

        print(result.axis_states)

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
