import cv2
import numpy as np


def normalize_image_lightness(image):
    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)


def convert_hls(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)


def select_white(image):
    lower = np.uint8([0, 187, 0])
    upper = np.uint8([255, 255, 51])
    return cv2.inRange(image, lower, upper)


def handle_frame(frame):
    normalized_image = normalize_image_lightness(frame)
    hls_image = convert_hls(normalized_image)
    white_mask = select_white(hls_image)
    result = cv2.bitwise_and(frame, frame, mask=white_mask)

    cv2.imshow('Preview', result)
