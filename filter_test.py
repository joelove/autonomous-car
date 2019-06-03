import time
import cv2

from utilities.stream_pipelines import gstreamer_pipeline
from utilities.image_filters import apply_default_filters

capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

while capture.isOpened():
    success, frame = capture.read()

    frame = apply_default_filters(frame)

    if success:
        cv2.imshow(frame)
        cv2.waitKey(0)

    time.sleep(0.1)
