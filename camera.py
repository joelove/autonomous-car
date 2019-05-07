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

        self.frames = Queue()

        self.thread = Thread(target=self.begin_capture, args=(self.frames,))
        self.thread.daemon = True
        self.thread.start()

        time.sleep(0.1) # warm up


    def begin_capture(self, frames):
        stream = PiRGBArray(self.camera)

        for frame in self.camera.capture_continuous(stream, format='bgr'):
            stream.truncate()
            stream.seek(0)

            frame = stream.array
            # frame = apply_filters(stream.array)
            frames.put(frame)
