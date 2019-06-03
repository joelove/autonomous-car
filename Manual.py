import time
import json
import config
import numpy as np

from PIL import Image
from Controller import Controller
from Vehicle import Vehicle

from utilities.image_filters import apply_default_filters


class Manual(Vehicle):
    def __init__(self, **kwargs):
        super().__init__()

        self.capture = kwargs["capture"]
        self.controller = Controller()


    def save_data_record(self, angle, throttle, frame):
        print("Save")
        timestamp = time.time()

        frame_filename = str(timestamp) + '_frame.jpg'
        frame_path = config.DATA_PATH + '/' + frame_filename
        record_path = config.DATA_PATH + '/' + str(timestamp) + '_record.json'

        filtered_frame = apply_default_filters(frame)

        frame_image = Image.fromarray(filtered_frame)
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

                if config.FIXED_SPEED_MODE and throttle_interval > 0:
                    throttle_interval = config.FIXED_SPEED_INTERVAL

                if throttle_interval and not steering_interval:
                    throttle_interval += config.THROTTLE_STRAIGHT_AUGMENTATION

                angle = self.interval_to_steering_angle(steering_interval)
                throttle = self.interval_to_throttle(throttle_interval)

                self.servos.set_angle(angle)
                self.servos.set_throttle(throttle)

                if button_states:
                    record = button_states["a"]

                    if record and self.capture:
                        while not self.camera.frames.empty():
                            latest_frame = self.camera.frames.get_nowait()

                        if latest_frame.size:
                            self.save_data_record(steering_interval, throttle_interval, latest_frame)

            time.sleep(tick_length - ((time.time() - start_time) % tick_length))
