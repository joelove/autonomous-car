import time
import cv2
import config

from threading import Thread
from multiprocessing import Queue
from utilities.stream_pipelines import gstreamer_pipeline


class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        self.capture.open()

        self.frames = Queue()
        self.thread = Thread(target=self.capture_continuous, daemon=True, args=(self.frames,))
        self.thread.start()


    def capture_continuous(self, frames):
        tick_length = (1.0 / config.DRIVE_LOOP_HZ) / 2

        while True:
            start_time = time.time()

            if not frames.full():
                success, frame = self.capture.read();

                if success:
                    frames.put_nowait(frame)

            time.sleep(tick_length - ((time.time() - start_time) % tick_length))
