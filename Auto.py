import numpy as np
import config
import time
import cv2

from Vehicle import Vehicle

from tensorflow.keras.models import model_from_json
from utilities.image_filters import apply_default_filters


class Auto(Vehicle):
    def __init__(self):
        super().__init__()

        json_file = open("model.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()

        self.model = model_from_json(loaded_model_json)
        self.model.load_weights("model.h5")


    def process_frame(self, frame):
        filtered_frame = apply_default_filters(frame)
        frame_array = filtered_frame.reshape((1,) + filtered_frame.shape + (1,))

        prediction = self.model.predict(frame_array)
        steering_interval, throttle_interval = np.array(prediction).reshape(2,)

        if config.FIXED_SPEED_MODE:
            throttle_interval = config.FIXED_SPEED_INTERVAL

        if throttle_interval and not steering_interval:
            throttle_interval += config.THROTTLE_STRAIGHT_INCREASE

        angle = self.interval_to_steering_angle(steering_interval)
        throttle = self.interval_to_throttle(throttle_interval)

        self.servos.set_angle(angle)
        self.servos.set_throttle(throttle)


    def drive(self):
        print('>> Autonomous driving <<')

        tick_length = 1.0 / config.DRIVE_LOOP_HZ

        while True:
            success, frame = self.camera.read()

            if not success:
                continue

            start_time = time.time()

            self.process_frame(frame)

            elapsed_time = time.time() - start_time

            time.sleep(tick_length - elapsed_time % tick_length)
