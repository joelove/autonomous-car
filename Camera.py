import cv2

from threading import Thread
from multiprocessing import Queue
from utilities.stream_pipelines import gstreamer_pipeline


class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        self.frames = Queue()
        self.thread = Thread(target=self.capture_continuous, daemon=True, args=(self.frames,))
        self.thread.start()


    def capture_continuous(self, frames):
        while self.capture.isOpened():
            if frames.full():
                _, frame = self.capture.read();
                frames.put_nowait(frame)
