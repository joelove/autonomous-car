import sys
import time
import cv2
import config
import signal

from threading import Thread
from multiprocessing import Queue
from utilities.stream_pipelines import gstreamer_pipeline


class Camera:
    def __init__(self):
        signal.signal(signal.SIGINT, self.handle_sigint)

        self.capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

        self.frames = Queue()
        self.thread = Thread(target=self.capture_continuous, daemon=True, args=(self.frames,))
        self.thread.start()


    def handle_sigint(self, signal, frame):
        self.capture.release()
        sys.exit(0)


    def capture_continuous(self, frames):
        tick_length = 1.0 / config.CAMERA_CAPTURE_RATE

        while self.capture.isOpened():
            start_time = time.time()

            if not frames.full():
                success, frame = self.capture.read()

                if success:
                    frames.put_nowait(frame)

            time.sleep(tick_length - ((time.time() - start_time) % tick_length))
