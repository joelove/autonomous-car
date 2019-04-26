import cv2
import numpy as np
import config

from keras.models import model_from_json
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


    def drive(self):
        print('>> Autonomous driving <<')

        while True:
            frame = self.camera.capture()
            prediction = self.model.predict(frame)

            print(prediction)

            self.servos.set_throttle(config.THROTTLE_MAX) # trololololol
