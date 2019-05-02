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


    def axis_to_unit_interval(self, axis):
        return (axis + 1) / 2


    def number_to_exponential(self, axis):
        cube_axis = axis ** 3
        exponential_axis = -cube_axis if axis <= 0 else cube_axis

        return exponential_axis


    def axis_to_angle(self, axis):
        exponential_axis = self.number_to_exponential(axis)
        exponential_interval = self.axis_to_unit_interval(exponential_axis)
        steering_angle = exponential_interval * config.STEERING_RANGE
        actuation_range = self.servos.steering_servo.actuation_range
        range_difference = actuation_range - config.STEERING_RANGE
        steering_lead = range_difference / 2
        angle = actuation_range - steering_lead - steering_angle

        return angle


    def axis_to_throttle(self, axis):
        interval = self.axis_to_unit_interval(axis)
        exponential_interval = self.number_to_exponential(interval)

        if not exponential_interval:
            return exponential_interval

        throttle_range = config.THROTTLE_MAX - config.THROTTLE_MIN
        throttle = config.THROTTLE_MIN + exponential_interval * throttle_range

        return throttle


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


    def steering_axis_to_interval(self, axis):
        steering_exponential_axis = self.number_to_exponential(axis)

        return axis

    def throttle_axis_to_interval(self, axis):
        throttle_interval = self.axis_to_unit_interval(axis)
        throttle_exponential_interval = self.number_to_exponential(throttle_interval)

        return throttle_exponential_interval


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
                left_stick_x_axis = axis_states["left_stick_x"]
                right_trigger_axis = axis_states["right_trigger"]

                steering_interval = self.steering_axis_to_interval(left_stick_x_axis)
                throttle_interval = self.throttle_axis_to_interval(right_trigger_axis)

                print('Steering interval', steering_interval)
                print('Throttle interval', throttle_interval)

                angle = self.axis_to_angle(left_stick_x_axis)
                throttle = self.axis_to_throttle(right_trigger_axis)

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
