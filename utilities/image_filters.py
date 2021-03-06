import cv2
import numpy as np
import config


def warp_by_shape(image, source_shape, destination_shape=[(0, 0), (1, 0), (1, 1), (0, 1)]):
    image_dimensions = tuple(reversed(image.shape))

    source_points = np.float32(source_shape) * np.float32(image_dimensions)
    destination_points = np.float32(destination_shape) * np.float32(image_dimensions)

    transformation = cv2.getPerspectiveTransform(source_points, destination_points)

    return cv2.warpPerspective(image, transformation, image_dimensions)


def crop_hood(image):
    image_height, image_width = image.shape

    first_third = int(0.275 * np.float32(image_width))
    last_third = int(0.725 * np.float32(image_width))

    left_image = image[:, :first_third+2]
    right_image = image[:, last_third:]
    center_image = image[:, first_third:last_third]

    hood_height = 0.3
    horizon_height = 0.4
    peripheral_height = 0.5

    left_horizon_shape = [(0, peripheral_height), (1, horizon_height), (1, 1), (0, 1)]
    right_horizon_shape = [(0, horizon_height), (1, peripheral_height), (1, 1), (0, 1)]
    center_horizon_shape = [(0, horizon_height), (1, horizon_height), (1, 1), (0, 1)]

    left_hood_shape = [(0, 0), (1, 0), (1, hood_height), (0, 1)]
    right_hood_shape = [(0, 0), (1, 0), (1, 1), (0, hood_height)]
    center_hood_shape = [(0, 0), (1, 0), (1, hood_height), (0, hood_height)]

    left_warped = warp_by_shape(left_image, left_horizon_shape)
    left_warped = warp_by_shape(left_warped, left_hood_shape)
    left_warped = warp_by_shape(left_warped, right_hood_shape)

    right_warped = warp_by_shape(right_image, right_horizon_shape)
    right_warped = warp_by_shape(right_warped, right_hood_shape)
    right_warped = warp_by_shape(right_warped, left_hood_shape)

    center_warped = warp_by_shape(center_image, center_horizon_shape)
    center_warped = warp_by_shape(center_warped, center_hood_shape)

    left_cropped = left_warped[:, :-2]
    right_cropped = right_warped[:, :]
    center_cropped = center_warped[:, :]

    vanishing_point_shape = [(0.2, 0.1), (0.8, 0.1), (1, 1), (0, 1)]

    stiched_image = np.concatenate((left_cropped, center_cropped, right_cropped), axis=1)

    return stiched_image


def resize(image):
    output_image = cv2.resize(image, config.CAMERA_FINAL_RESOLUTION, interpolation=cv2.INTER_NEAREST)

    return output_image


def apply_clahe(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahed_image = clahe.apply(image)

    return clahed_image


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
    image = crop_hood(image)
    image = resize(image)
    image = apply_clahe(image)
    image = reduce_noise(image)

    return image
