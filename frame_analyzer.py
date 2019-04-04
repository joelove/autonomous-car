import cv2
import numpy as np


def convert_hls(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)


def convert_gray_scale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def apply_smoothing(image, kernel_size=9):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def detect_edges(image, low_threshold=50, high_threshold=150):
    return cv2.Canny(image, low_threshold, high_threshold)


def hough_lines(image):
    return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)


def filter_region(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)

    return cv2.bitwise_and(image, mask)


def select_region(image):
    y_height, x_height = image.shape[:2]

    bottom_left  = [x_height * 0,   y_height * 1]
    middle_left  = [x_height * 0,   y_height * 0.5]
    top_left     = [x_height * 0.5, y_height * 0]
    top_right    = [x_height * 0.5, y_height * 0]
    middle_right = [x_height * 1,   y_height * 0.5]
    bottom_right = [x_height * 1,   y_height * 1]

    vertices = np.array([[bottom_left, middle_left, top_left, top_right, middle_right, bottom_right]], dtype=np.int32)

    return filter_region(image, vertices)


def normalize_image_lightness(image):
    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))

    return cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)


def select_white(image):
    lower = np.uint8([0, 187, 0])
    upper = np.uint8([255, 255, 51])

    return cv2.inRange(image, lower, upper)


def handle_frame(frame):
    normalized_image = normalize_image_lightness(frame)
    hls_image = convert_hls(normalized_image)
    white_mask = select_white(hls_image)
    masked_image = cv2.bitwise_and(frame, frame, mask=white_mask)
    greyscale_image = convert_gray_scale(masked_image)
    smooth_image = apply_smoothing(greyscale_image)
    image_region = select_region(smooth_image)
    image_edges = detect_edges(image_region)
    # image_lines = hough_lines(image_edges)

    cv2.imshow('Preview', image_edges)
