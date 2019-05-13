import cv2
import time
import numpy as np


def perspective_warp(image):
    image_dimensions = tuple(reversed(image.shape))

    source_shape = [(0, 0.375), (1, 0.375), (1, 1), (0, 1)]
    destination_shape = [(0, 0), (1, 0), (1, 1), (0, 1)]

    source_points = np.float32(source_shape) * np.float32(image_dimensions)
    destination_points = np.float32(destination_shape) * np.float32(image_dimensions)

    transformation = cv2.getPerspectiveTransform(source_points, destination_points)

    return cv2.warpPerspective(image, transformation, image_dimensions)


def reduce_noise(image, ksize=3):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


def rgb_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def calculate_image_derivatives(image):
    scharr_x = cv2.Scharr(image, cv2.CV_16S, 1, 0)
    scharr_y = cv2.Scharr(image, cv2.CV_16S, 0, 1)

    x_derivative = cv2.convertScaleAbs(scharr_x)
    y_derivative = cv2.convertScaleAbs(scharr_y)

    return x_derivative, y_derivative


def detect_edges(image):
    x_derivative, y_derivative = calculate_image_derivatives(image)
    edges = cv2.addWeighted(x_derivative, 0.5, y_derivative, 0.5, 0)

    return edges


def apply_default_filters(image):
    image = rgb_to_grayscale(image)
    image = reduce_noise(image)
    image = perspective_warp(image)

    return image
