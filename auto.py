import numpy as np
import config
import time

from drive import Drive

from tensorflow.keras.models import model_from_json
from image_processor import apply_filters


class Auto(Drive):
    def __init__(self):
        super().__init__() 

        json_file = open("model.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()

        self.model = model_from_json(loaded_model_json)
        self.model.load_weights("model.h5")


    def process_frame(self, frame):
        filtered_frame = apply_filters(frame)
        frame_array = filtered_frame.reshape((1,) + filtered_frame.shape + (1,))
        frame_array = frame_array / 255.0

        prediction = self.model.predict(frame_array)
        steering_interval, throttle_interval = np.array(prediction).reshape(2,)

        angle = self.interval_to_steering_angle(steering_interval)
        throttle = self.interval_to_throttle(0.5)

        self.servos.set_angle(angle)
        self.servos.set_throttle(throttle)


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
