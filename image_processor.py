import cv2
import numpy as np

from funcy import compose


reverse_tuple = compose(tuple, reversed)


def perspective_warp(image):
    image_dimensions = reverse_tuple(image.shape)

    source_shape = [(0.6, 0.4), (1, 0.45), (1, 1), (0, 1), (0, 0.45), (0.4, 0.4)]
    destination_shape = [(0, 0), (1, 0.45), (1, 1), (0, 1), (0, 0.45), (1, 0)]

    source_pixels = np.float32(source_shape) * np.float32(image_dimensions)
    destination_pixels = np.float32(destination_shape) * np.float32(image_dimensions)

    transformation = cv2.getPerspectiveTransform(source_pixels, destination_pixels)

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


def apply_filters(image):
    filter = compose(perspective_warp, detect_edges, rgb_to_grayscale, reduce_noise)

    return filter(image)
