import time
import cv2

from utilities.stream_pipelines import gstreamer_pipeline

capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

while capture.isOpened():
    success, frame = capture.read()

    if success:
        cv2.imshow(frame)

    time.sleep(0.1)
