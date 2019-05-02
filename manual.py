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
        cube_axis = axis ** 3
        exponential_axis = -cube_axis if axis else cube_axis

        print(exponential_axis)

        exponential_interval = self.axis_to_unit_interval(exponential_axis)
        steering_angle = exponential_interval * config.STEERING_RANGE
        actuation_range = self.servos.steering_servo.actuation_range
        range_difference = actuation_range - config.STEERING_RANGE
        steering_lead = range_difference / 2
        angle = actuation_range - steering_lead - steering_angle

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

        frame_filename = str(timestamp) + '_frame.jpg'
        frame_path = config.DATA_PATH + '/' + frame_filename
        record_path = config.DATA_PATH + '/' + str(timestamp) + '_record.json'

        frame_image = Image.fromarray(frame)
        frame_image.save(frame_path)

        data = {
            "timestamp": timestamp,
            "angle": angle,
            "throttle": throttle,
            "frame_filename": frame_filename
        }

        with open(record_path, 'w') as record_file:
            json.dump(data, record_file)

        print('Saved record:', timestamp, throttle, angle)


    def drive(self):
        print('>> Manual driving <<')
        print('Data capture: ' + str(self.capture))

        tick_length = 1.0 / config.DRIVE_LOOP_HZ

        joystick_state = ({}, {})
        latest_frame = np.array([])

        while True:
            start_time = time.time()

            while not self.controller.joystick_state.empty():
                joystick_state = self.controller.joystick_state.get_nowait()

            axis_states, button_states = joystick_state

            if axis_states:
                angle = self.axis_to_angle(axis_states["left_stick_x"])
                throttle = self.axis_to_throttle(axis_states["right_trigger"])

                self.servos.set_angle(angle)
                self.servos.set_throttle(throttle)

                if button_states:
                    record = button_states["a"]

                    if record and self.capture:
                        while not self.camera.frames.empty():
                            latest_frame = self.camera.frames.get_nowait()

                        if latest_frame.size:
                            self.save_data_record(angle, throttle, latest_frame)

            time.sleep(tick_length - ((time.time() - start_time) % tick_length))
