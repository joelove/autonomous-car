import math
import cv2
import numpy as np


# cv2.resize(image, dimensions, interpolation=cv2.INTER_NEAREST)


def warp_by_shape(image, source_shape, destination_shape):
    image_dimensions = tuple(reversed(image.shape))

    source_points = np.float32(source_shape) * np.float32(image_dimensions)
    destination_points = np.float32(destination_shape) * np.float32(image_dimensions)

    transformation = cv2.getPerspectiveTransform(source_points, destination_points)

    return cv2.warpPerspective(image, transformation, image_dimensions)


def crop_hood(image):
    image_height, image_width = image.shape

    first_third = math.floor(0.275 * np.float32(image_width))
    last_third = math.floor(0.725 * np.float32(image_width))

    left_image = image[:, :first_third+2]
    right_image = image[:, last_third:]
    center_image = image[:, first_third:last_third]

    hood_height = 0.315

    original_image_shape = [(0, 0), (1, 0), (1, 1), (0, 1)]
    cropped_image_shape = [(0, 0), (1, 0), (1, hood_height), (0, hood_height)]

    horizon_height = 0.075
    peripheral_height = 0.2

    left_horizon_shape = [(0, peripheral_height), (1, horizon_height), (1, 1), (0, 1)]
    right_horizon_shape = [(0, horizon_height), (1, peripheral_height), (1, 1), (0, 1)]
    center_horizon_shape = [(0, horizon_height), (1, horizon_height), (1, 1), (0, 1)]

    left_hood_shape = [(0, 0), (1, 0), (1, hood_height), (0, 1)]
    right_hood_shape = [(0, 0), (1, 0), (1, 1), (0, hood_height)]

    left_warped = warp_by_shape(left_image, left_horizon_shape, original_image_shape)
    left_warped = warp_by_shape(left_warped, left_hood_shape, cropped_image_shape)

    right_warped = warp_by_shape(right_image, right_horizon_shape, original_image_shape)
    right_warped = warp_by_shape(right_warped, right_hood_shape, cropped_image_shape)

    center_warped = warp_by_shape(center_image, center_horizon_shape, original_image_shape)

    hood_y = int(hood_height * np.float32(image_height))

    left_cropped = left_warped[:hood_y, :-2]
    right_cropped = right_warped[:hood_y, :]
    center_cropped = center_warped[:hood_y, :]

    return np.concatenate((left_cropped, center_cropped, right_cropped), axis=1)
