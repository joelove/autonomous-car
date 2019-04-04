import cv2

def handle_frame(frame):
    grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normalized_image = cv2.normalize(grayscale_image, None, beta=255, norm_type=cv2.NORM_MINMAX)

    # blurred_image = cv2.medianBlur(normalized_image, 7)
    # ret, thresh = cv2.threshold(blurred_image, 180, 255, 0)

    thresh = cv2.adaptiveThreshold(normalized_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)

    cv2.imwrite('test.png', thresh)

    # cv2.imshow('frame', thresh)

    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.fillPoly(frame, contours, color=(0, 255, 0))
    # cv2.imshow('frame', frame)
