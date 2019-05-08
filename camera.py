import time
import math
import config

from picamera import PiCamera
from picamera.array import PiRGBArray

from threading import Thread
from multiprocessing import Queue


class Camera:
    def __init__(self):
        self.camera = PiCamera(
            sensor_mode=4,
            resolution=config.CAMERA_RESOLUTION,
            framerate=config.CAMERA_FRAMERATE)

        self.frames = Queue()

        time.sleep(2) # warm up

        self.thread = Thread(target=self.start, daemon=True, args=(self.frames,))
        self.thread.start()


    def start(self, frames):
        stream = PiRGBArray(self.camera)

        for frame in self.camera.capture_continuous(stream, format='bgr', use_video_port=True):
            stream.truncate()
            stream.seek(0)

            if not frames.full():
                frames.put_nowait(frame)
