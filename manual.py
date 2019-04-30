import time
import json
import config

from camera import Camera
from controller import Controller
from servo_driver import ServoDriver


class Manual:
    def __init__(self, **kwargs):
        self.capture = kwargs["capture"]
        self.camera = Camera()
        self.servos = ServoDriver()


    def axis_to_unit_interval(self, range):
        return (range + 1) / 2


    def axis_to_angle(self, axis):
        interval = self.axis_to_unit_interval(axis)
        angle = config.STEERING_RANGE - interval * config.STEERING_RANGE

        return angle


    def axis_to_throttle(self, axis):
        interval = self.axis_to_unit_interval(axis)

        if interval:
            throttle_range = config.THROTTLE_MAX - config.THROTTLE_MIN
            throttle = config.THROTTLE_MIN + interval * throttle_range

            return throttle

        return interval

    def axis_to_reverse_throttle(self, axis):
        throttle = self.axis_to_throttle(axis)

        return throttle * -1


    def save_data_record(self, angle, throttle, frame):
        timestamp = time.time()

        with open(config.DATA_PATH + '/' + str(timestamp) + '_record.json', 'w') as record_file:
            json.dump({ timestamp, throttle, angle, frame }, record_file)
            print(timestamp, throttle, angle)


    def process_controller_state(self, controller_state):
        axis_states, button_states = controller_state

        angle = self.axis_to_angle(axis_states["left_stick_x"])
        throttle = self.axis_to_throttle(axis_states["right_trigger"])
        reverse_throttle = self.axis_to_reverse_throttle(axis_states["left_trigger"])

        record = button_states["a"]

        if record and self.capture:
            frame = json.dumps(self.camera.capture().tolist())
            self.save_data_record(angle, throttle, frame)

        self.servos.set_angle(angle)
        self.servos.set_throttle(throttle)

        if not throttle:
            self.servos.set_throttle(reverse_throttle)


    def drive(self):
        print('>> Manual driving <<')
        print('Data capture: ' + str(self.capture))

        controller = Controller()
        controller.read(self.process_controller_state)
