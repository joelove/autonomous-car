import cv2
import numpy as np


def undistort_image():
    obj_pts = np.zeros((6*9, 3), np.float32)
    obj_pts[:,:2] = np.mgrid[0:9, 0:6].T.reshape(-1,2)

    objpoints = []
    imgpoints = []

    images = glob.glob('camera_calibration/calibration_images/*.jpg')

    for indx, fname in enumerate(images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

        if ret == True:
            objpoints.append(obj_pts)
            imgpoints.append(corners)

    img_size = (img.shape[1], img.shape[0])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
    dst = cv2.undistort(img, mtx, dist, None, mtx)

    dist_pickle = {}
    dist_pickle['mtx'] = mtx
    dist_pickle['dist'] = dist

    pickle.dump( dist_pickle, open('camera_calibration/calibration_pickle.p', 'wb') )


def undistort(img, calibration_directory='camera_calibration/calibration_pickle.p'):
    with open(calibration_directory, mode='rb') as f:
        file = pickle.load(f)
        mtx = file['mtx']
        dist = file['dist']
        dst = cv2.undistort(img, mtx, dist, None, mtx)
        # cv2.imwrite('camera_calibration/test_calibration.jpg', dst)
        return dst
