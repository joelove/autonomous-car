import time
import config

from joystick import Joystick
from threading import Thread
from multiprocessing import Queue
from adafruit_servokit import ServoKit


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

        if axis_states:
            steering_angle = axis_states['x']

            kit = ServoKit(channels=16)

            servo_angle = int(((steering_angle + 1.0) / 2) * 180)

            print(servo_angle)

            steering_servo = kit.servo[config.STEERING_CHANNEL]
            steering_servo.angle = servo_angle

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))
