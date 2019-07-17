import time
import json
import config
import numpy as np

from PIL import Image
from Controller import Controller
from Vehicle import Vehicle
from Auto import Auto

from utilities.image_filters import apply_default_filters


class Manual(Vehicle):
    def __init__(self, **kwargs):
        super().__init__()

        self.capture = kwargs["capture"]
        self.controller = Controller()


    def save_data_record(self, angle, throttle, frame):
        timestamp = time.time()

        frame_filename = str(timestamp) + '_frame.jpg'
        raw_filename = str(timestamp) + '_raw.jpg'

        frame_path = config.DATA_PATH + '/' + frame_filename
        raw_path = config.DATA_PATH + '/' + raw_filename
        record_path = config.DATA_PATH + '/' + str(timestamp) + '_record.json'

        filtered_frame = apply_default_filters(frame)

        frame_image = Image.fromarray(filtered_frame)
        frame_image.save(frame_path)

        raw_image = Image.fromarray(frame)
        raw_image.save(raw_path)

        data = {
            "timestamp": timestamp,
            "angle": angle,
            "throttle": throttle,
            "frame_filename": frame_filename,
            "raw_frame_filename": raw_filename
        }

        with open(record_path, 'w') as record_file:
            json.dump(data, record_file)

        print('Saved record:', timestamp, throttle, angle)


    def switch_mode(self):
        self.release_all()

        vehicle = Auto()
        vehicle.drive()


    def drive(self):
        print('>> Manual driving <<')
        print('Data capture: ' + 'Yes' if self.capture else 'No')

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

                if throttle_interval < config.THROTTLE_SHIFT:
                    if config.FIXED_SPEED_MODE:
                        throttle_interval = config.FIXED_SPEED_INTERVAL

                    throttle_interval = self.throttle_angle_adjust(throttle_interval, steering_interval)

                angle = self.interval_to_steering_angle(steering_interval)
                throttle = self.interval_to_throttle(throttle_interval)

                self.servos.set_angle(angle)
                self.servos.set_throttle(throttle)

                if button_states:
                    record = button_states["a"]
                    switch_mode = button_states["start"]

                    if switch_mode:
                        self.switch_mode()
                        break

                    if record and self.capture:
                        success, latest_frame = self.camera.read()

                        if success:
                            self.save_data_record(steering_interval, throttle_interval, latest_frame)

            time.sleep(tick_length - ((time.time() - start_time) % tick_length))
