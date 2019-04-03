import cv2
import time

def capture(handle_frame):
    video_capture = cv2.VideoCapture(0)

    while True:
        video_capture.grab()
        ret, frame = video_capture.retrieve()

        if (ret == False):
            break;

        image = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

        handle_frame(image)

        time.sleep(0)

    video_capture.release()
