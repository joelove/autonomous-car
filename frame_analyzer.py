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
    return cv2.HoughLinesP(image, rho=0.5, theta=np.pi/180, threshold=20, minLineLength=30, maxLineGap=20)


def filter_region(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)

    return cv2.bitwise_and(image, mask)


def select_region(image):
    y_height, x_height = image.shape[:2]

    bottom_left  = [x_height * 0,   y_height * 1]
    middle_left  = [x_height * 0,   y_height * 0.5]
    top_left     = [x_height * 0.35, y_height * 0]
    top_right    = [x_height * 0.65, y_height * 0]
    middle_right = [x_height * 1,   y_height * 0.5]
    bottom_right = [x_height * 1,   y_height * 1]

    vertices = np.array([[bottom_left, middle_left, top_left, top_right, middle_right, bottom_right]], dtype=np.int32)

    return filter_region(image, vertices)


def normalize_image_lightness(image):
    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    lightness, a, b = cv2.split(lab_image)
    normalized_lightness = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(lightness)
    normalized_image = cv2.merge((normalized_lightness, a, b))

    return cv2.cvtColor(normalized_image, cv2.COLOR_LAB2RGB)


def select_white(image):
    lower = np.uint8([0, 187, 0])
    upper = np.uint8([255, 255, 51])

    return cv2.inRange(image, lower, upper)


def average_slope_intercept(lines):
    left_lines    = []
    left_weights  = []
    right_lines   = []
    right_weights = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            if x2==x1:
                continue

            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            length = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

            if slope < 0:
                left_lines.append((slope, intercept))
                left_weights.append((length))
            else:
                right_lines.append((slope, intercept))
                right_weights.append((length))

    left_lane  = np.dot(left_weights,  left_lines)  / np.sum(left_weights)  if len(left_weights)  > 0 else None
    right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None

    return left_lane, right_lane


def make_line_points(y1, y2, line):
    if line is None:
        return None

    slope, intercept = line

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    y1 = int(y1)
    y2 = int(y2)

    return ((x1, y1), (x2, y2))


def get_lanes(image_lines, image_height):
    left_lane, right_lane = average_slope_intercept(image_lines)

    y1 = image_height
    y2 = y1 * 0.6

    left_line  = make_line_points(y1, y2, left_lane)
    right_line = make_line_points(y1, y2, right_lane)

    return left_line, right_line


def get_image_height(image):
    return image.shape[0]


def draw_line(image, line, color):
    if line is not None:
        cv2.line(image, *line, color, 20)


def handle_frame(frame):
    normalized_image = normalize_image_lightness(frame)
    hls_image = convert_hls(normalized_image)
    white_mask = select_white(hls_image)
    masked_image = cv2.bitwise_and(normalized_image, normalized_image, mask=white_mask)
    greyscale_image = convert_gray_scale(masked_image)
    image_region = select_region(greyscale_image)
    smooth_image = apply_smoothing(image_region)
    image_height = get_image_height(smooth_image)
    image_edges = detect_edges(smooth_image)
    image_lines = hough_lines(image_edges)
    left_lane, right_lane = get_lanes(image_lines, image_height)

    draw_line(frame, left_lane, (255, 0, 0))
    draw_line(frame, right_lane, (0, 255, 0))

    # for line in image_lines:
    #     x1, y1, x2, y2 = line[0]
    #     cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('Preview', frame)
