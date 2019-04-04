import cv2

def capture(handle_frame):
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
