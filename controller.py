import time

from joystick import Joystick
from multiprocessing import Process


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ

def polling_loop(joystick):
    while True:
        start_time = time.time()

        print(joystick.axis_states)

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))


def read_controller():
    joystick = Joystick()

    process = Process(target=polling_loop, args=(joystick,))
    process.start()

    joystick.init()
    joystick.begin_polling()
