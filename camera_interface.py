import os
import time

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    import cv2


def is_linux():
    return os.path.exists('/proc/cpuinfo')


def capture_webcam(handle_frame):
    video_capture = cv2.VideoCapture(0)

    while True:
        video_capture.grab()
        ret, frame = video_capture.retrieve()

        if (ret == False):
            break

        handle_frame(frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    video_capture.release()

    cv2.destroyAllWindows()


def capture_picam(handle_frame):
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 10

    rawCapture = PiRGBArray(camera, size=camera.resolution)

    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        handle_frame(frame.array)
        rawCapture.truncate(0)
        break


def capture(handle_frame):
    if is_linux():
        capture_picam(handle_frame)
    else:
        capture_webcam(handle_frame)
