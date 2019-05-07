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

        time.sleep(0.1) # warm up


    def capture(self):
        stream = PiRGBArray(self.camera)
        self.camera.capture(stream, format='bgr')
        frame = apply_filters(stream.array)

        return frame
