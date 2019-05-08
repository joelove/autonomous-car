import numpy as np
import config
import time

from tensorflow.keras.models import model_from_json
from servo_driver import ServoDriver
from camera import Camera
from image_processor import apply_filters


class Auto:
    def __init__(self):
        self.camera = Camera()
        self.servos = ServoDriver()

        json_file = open("model.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()

        self.model = model_from_json(loaded_model_json)
        self.model.load_weights("model.h5")


    def axis_to_unit_interval(self, axis):
        return (axis + 1) / 2


    def interval_to_steering_angle(self, interval):
        unit_interval = self.axis_to_unit_interval(interval)
        actual_angle = unit_interval * config.STEERING_RANGE
        actuation_range = self.servos.steering_servo.actuation_range
        range_difference = actuation_range - config.STEERING_RANGE
        steering_lead = range_difference / 2
        steering_angle = actuation_range - steering_lead - actual_angle

        return steering_angle


    def interval_to_throttle(self, interval):
        if not interval:
            return interval

        throttle_range = config.THROTTLE_MAX_PERCENT - config.THROTTLE_MIN_PERCENT
        throttle_percent = config.THROTTLE_MIN_PERCENT + interval * throttle_range
        throttle = throttle_percent / 100

        return throttle


    def process_frame(self, frame):
        filtered_frame = apply_filters(frame)
        frame_array = filtered_frame.reshape((1,) + filtered_frame.shape + (1,))
        frame_array = frame_array / 255.0

        prediction = self.model.predict(frame_array)
        steering_interval, throttle_interval = np.array(prediction).reshape(2,)

        angle = self.interval_to_steering_angle(steering_interval)
        throttle = self.interval_to_throttle(throttle_interval)

        self.servos.set_angle(angle)
        self.servos.set_throttle(0.25)


    def drive(self):
        print('>> Autonomous driving <<')

        tick_length = 1.0 / config.DRIVE_LOOP_HZ

        while True:
            frame = np.array([])

            while not self.camera.frames.empty():
                frame = self.camera.frames.get_nowait()

            if not frame.size:
                continue

            start_time = time.time()

            self.process_frame(frame)

            elapsed_time = time.time() - start_time

            time.sleep(tick_length - elapsed_time % tick_length)
