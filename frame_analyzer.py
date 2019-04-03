import cv2

def handle_frame(frame):
    grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normalized_image = cv2.normalize(grayscale_image, None, beta=255, norm_type=cv2.NORM_MINMAX)
    blurred_image = cv2.medianBlur(normalized_image, 5)

    ret, thresh = cv2.threshold(blurred_image, 170, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(frame, contours, -1, (255, 0, 255), 3)
    cv2.fillPoly(frame, contours, color=(0, 255, 0))
    cv2.imshow('frame', frame)
