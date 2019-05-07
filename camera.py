import time
import config

from picamera import PiCamera
from picamera.array import PiRGBArray

from threading import Thread
from multiprocessing import Queue
from image_processor import apply_filters


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = config.CAMERA_RESOLUTION
        self.camera.framerate = config.CAMERA_FRAMERATE

        self.stream = PiRGBArray(self.camera)

        time.sleep(0.1) # warm up


    def capture(self):
        self.stream.truncate(0)
        self.camera.capture(self.stream, format='bgr')

        return apply_filters(self.stream.array)
