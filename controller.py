import time
import config

from joystick import Joystick
from threading import Thread
from multiprocessing import Queue
from actuator import PCA9685


SAMPLE_HZ = 10
TICK_LENGTH = 1.0 / SAMPLE_HZ


def read_controller():
    joystick = Joystick()
    joystick.init()

    queue = Queue()

    thread = Thread(target=joystick.begin_polling, args=(queue,))
    thread.daemon = True
    thread.start()

    axis_states = {}

    while True:
        start_time = time.time()

        while not queue.empty():
            axis_states = queue.get_nowait()

        steering_angle = axis_states.x
        left_pulse = 290
        right_pulse = 490
        half_difference = (left_pulse - right_pulse) / 2
        pulse = (left_pulse + half_difference) + (steering_angle * half_difference)

        steering_controller = PCA9685(config.STEERING_CHANNEL)
        steering_controller.set_pulse(pulse)

        # throttle_value = axis_states.gas
        # throttle_controller = PCA9685(config.THROTTLE_CHANNEL)

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
