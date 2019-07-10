import numpy as np
import config
import time
import cv2

from Vehicle import Vehicle
from Controller import Controller

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

        self.controller = Controller()
        self.launched = False


    def process_frame(self, frame):
        filtered_frame = apply_default_filters(frame)
        frame_array = filtered_frame.reshape(
            (1,) + filtered_frame.shape + (1,))

        prediction = self.model.predict(frame_array)
        steering_interval, throttle_interval = np.array(prediction).reshape(2,)

        if config.FIXED_SPEED_MODE:
            throttle_interval = config.FIXED_SPEED_INTERVAL

        throttle_interval = self.throttle_angle_adjust(
            throttle_interval, steering_interval)

        angle = self.interval_to_steering_angle(steering_interval)
        throttle = self.interval_to_throttle(throttle_interval)

        if self.launched:
            self.servos.set_angle(angle)
            self.servos.set_throttle(throttle)
        else:
            self.servos.release()


    def drive(self):
        print('>> Autonomous driving <<')

        tick_length = 1.0 / config.DRIVE_LOOP_HZ
        joystick_state = ({}, {})

        self.model.predict(np.zeros((1,) + config.CAMERA_FINAL_RESOLUTION + (1,)))

        while True:
            start_time = time.time()

            while not self.controller.joystick_state.empty():
                joystick_state = self.controller.joystick_state.get_nowait()

            axis_states, button_states = joystick_state

            if button_states:
                launch = button_states["y"]
                stop = button_states["x"]

                if launch:
                    self.launched = True

                if stop:
                    self.launched = False

            success, frame = self.camera.read()

            if not success:
                continue

            self.process_frame(frame)

            elapsed_time = time.time() - start_time

            time.sleep(tick_length - elapsed_time % tick_length)
