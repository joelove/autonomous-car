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

        while True:
            self.camera.capture(stream, format='bgr')

            if not frames.full():
                frame = apply_filters(stream.array)
                frames.put_nowait(frame)

            stream.truncate(0)
