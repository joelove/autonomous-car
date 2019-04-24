import time

from joystick import Joystick
from multiprocessing import Process, Queue


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ


def read_controller():
    queue = Queue()

    joystick = Joystick()
    joystick.init()

    process = Process(target=joystick.begin_polling, args=(queue,))
    process.start()

    while True:
        start_time = time.time()

        print(queue.get_nowait())

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
