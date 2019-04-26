import time
import json
import numpy.core.multiarray
import cv2
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
        angle = interval * config.STEERING_RANGE

        return angle


    def axis_to_throttle(self, axis):
        interval = self.axis_to_unit_interval(axis)
        throttle = interval * config.THROTTLE_MAX

        return throttle


    def save_data_record(self, angle, throttle, frame_array):
        print(frame_array) #debug
        print(angle) # debug
        print(throttle) # debug

        timestamp = time.time()

        with open(config.DATA_PATH + '/' + timestamp + '_record.json', 'w') as record_file:
            json.dump({ timestamp, throttle, angle, frame_array }, record_file)


    def process_controller_state(self, controller_state):
        axis_states, button_states = controller_state

        angle = self.axis_to_angle(axis_states["left_stick_x"])
        throttle = self.axis_to_throttle(axis_states["right_trigger"])

        record = button_states["a"]

        if record and self.capture:
            frame_array = self.camera.capture()
            self.save_data_record(angle, throttle, frame_array)

        self.servos.set_angle(angle)
        self.servos.set_throttle(throttle)


    def drive(self):
        print('>> Manual driving <<')
        print('Data capture: ' + str(self.capture))

        controller = Controller()
        controller.read(self.process_controller_state)
