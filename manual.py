import time
import json
import config
import numpy as np

from PIL import Image
from camera import Camera
from controller import Controller
from servo_driver import ServoDriver


class Manual:
    def __init__(self, **kwargs):
        self.capture = kwargs["capture"]
        self.camera = Camera()
        self.controller = Controller()
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


    def save_data_record(self, angle, throttle, frame):
        timestamp = time.time()

        record_path = config.DATA_PATH + '/' + str(timestamp) + '_record.json'
        frame_path = config.DATA_PATH + '/' + str(timestamp) + '_frame.jpg'

        frame_image = Image.fromarray(frame)
        frame_image.save(frame_path)

        data = {
            "timestamp": timestamp,
            "angle": angle,
            "throttle": throttle,
            "frame_path": frame_path
        }

        with open(record_path, 'w') as record_file:
            json.dump(data, record_file)

        print(timestamp, throttle, angle)


    def drive(self):
        print('>> Manual driving <<')
        print('Data capture: ' + str(self.capture))

        joystick_state = None
        latest_frame = None
        tick_length = 1.0 / config.DRIVE_LOOP_HZ

        while True:
            start_time = time.time()

            joystick_state = ({}, {})

            while not self.controller.joystick_state.empty():
                joystick_state = self.controller.joystick_state.get_nowait()

            axis_states, button_states = joystick_state

            if axis_states:
                angle = self.axis_to_angle(axis_states["left_stick_x"])
                throttle = self.axis_to_throttle(axis_states["right_trigger"])

                if button_states:
                    record = button_states["a"]

                    if record and self.capture:
                        latest_frame = None

                        while not self.camera.frames.empty():
                            latest_frame = self.camera.frames.get_nowait()

                        if latest_frame:
                            self.save_data_record(angle, throttle, latest_frame)

                self.servos.set_angle(angle)
                self.servos.set_throttle(throttle)

            time.sleep(tick_length - ((time.time() - start_time) % tick_length))
