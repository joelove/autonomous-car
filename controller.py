import time

from joystick import Joystick
from threading import Thread
from multiprocessing import Queue


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ


def read_controller():
    joystick = Joystick()
    joystick.init()

    queue = Queue()

    thread = Thread(target=joystick.begin_polling, args=(queue,))
    thread.daemon = True
    thread.start()

    controller = {}

    while True:
        start_time = time.time()

        while not queue.empty():
            controller = queue.get_nowait()

        print('Throttle: ' + controller.throttle)
        print('Angle: ' + controller.angle)


        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
