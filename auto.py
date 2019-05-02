import cv2
import numpy as np
import config
import random
import glob
import json
import time

from tensorflow.keras.models import model_from_json
from servo_driver import ServoDriver
from camera import Camera


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


    def drive(self):
        print('>> Autonomous driving <<')

        frame_array = np.array([])

        tick_length = 1.0 / config.DRIVE_LOOP_HZ

        while True:
            start_time = time.time()
            while not self.camera.frames.empty():
                frame_array = self.camera.frames.get_nowait()

            if frame_array.size:
                frame_array = frame_array.reshape((1,) + frame_array.shape + (1,))
                frame_array = frame_array / 255.0

                prediction = self.model.predict(frame_array)

                steering_interval_prediction = prediction[0][0][0]
                throttle_interval_prediction = prediction[1][0][0]

                print('steering prediction', steering_interval_prediction)
                print('throttle prediction', throttle_interval_prediction)

                angle = self.interval_to_steering_angle(steering_interval_prediction)
                throttle = self.interval_to_throttle(throttle_interval_prediction)

                self.servos.set_angle(angle)
                self.servos.set_throttle(throttle)


            time.sleep(tick_length - ((time.time() - start_time) % tick_length))

            # self.servos.set_throttle(config.THROTTLE_MAX) # trololololol
