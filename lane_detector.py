import cv2
import numpy as np


# def undistort_image():
#     obj_pts = np.zeros((6*9, 3), np.float32)
#     obj_pts[:,:2] = np.mgrid[0:9, 0:6].T.reshape(-1,2)
#
#     objpoints = []
#     imgpoints = []
#
#     images = glob.glob('camera_calibration/calibration_images/*.jpg')
#
#     for indx, fname in enumerate(images):
#         img = cv2.imread(fname)
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
#
#         if ret == True:
#             objpoints.append(obj_pts)
#             imgpoints.append(corners)
#
#     img_size = (img.shape[1], img.shape[0])
#     ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
#     dst = cv2.undistort(img, mtx, dist, None, mtx)
#
#     dist_pickle = {}
#     dist_pickle['mtx'] = mtx
#     dist_pickle['dist'] = dist
#
#     pickle.dump( dist_pickle, open('camera_calibration/calibration_pickle.p', 'wb') )


# def undistort(img, calibration_directory='camera_calibration/calibration_pickle.p'):
#     with open(calibration_directory, mode='rb') as f:
#         file = pickle.load(f)
#         mtx = file['mtx']
#         dist = file['dist']
#         dst = cv2.undistort(img, mtx, dist, None, mtx)
#         # cv2.imwrite('camera_calibration/test_calibration.jpg', dst)
#         return dst


def perspective_warp(image,
        dst_size=(1280,720),
        src=np.float32([(0.43, 0.65), (0.58, 0.65), (0.1, 1), (1, 1)]),
        dst=np.float32([(0, 0), (1, 0), (0, 1), (1, 1)])):
    image_size = np.float32([(image.shape[1], image.shape[0])])
    src = src * image_size
    dst = dst * np.float32(dst_size)
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(image, M, dst_size)
    return warped


def reduce_noise(image, ksize=3):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


def rgb_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def calculate_image_derivatives(image):
    scharr_x = cv2.Scharr(image, cv2.CV_16S, 1, 0)
    scharr_y = cv2.Scharr(image, cv2.CV_16S, 0, 1)

    # # A kernel size of 5 will be more computationally expensive but potentially more useful
    # sobel_x = cv2.Sobel(img, cv2.CV_16S, 1, 0, ksize=5)
    # sobel_y = cv2.Sobel(img, cv2.CV_16S, 0, 1, ksize=5)

    x_derivative = cv2.convertScaleAbs(scharr_x)
    y_derivative = cv2.convertScaleAbs(scharr_y)

    return x_derivative, y_derivative


def detect_edges(image):
    x_derivative, y_derivative = calculate_image_derivatives(image)
    edges = cv2.addWeighted(x_derivative, 0.5, y_derivative, 0.5, 0)

    return edges


def convert_to_8_bit(image):
    return cv2.convertScaleAbs(image)


def detect_lanes(image):
    denoised_image = reduce_noise(image)
    greyscale_image = rgb_to_grayscale(denoised_image)
    perspective_image = perspective_warp(greyscale_image)
    edges = detect_edges(perspective_image)

    histogram = cv2.calcHist([edges], [0], None, [256], [0, 256])

    print(histogram)

    # cv2.imshow('Preview', edges)
