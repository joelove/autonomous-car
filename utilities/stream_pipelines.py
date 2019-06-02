import os
import sys

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
root_dir = os.path.join(script_dir, os.pardir)

sys.path.append(root_dir)

import config


def gstreamer_pipeline():
    return (
        'nvarguscamerasrc ! '
        'video/x-raw(memory:NVMM), '
        'width=%d, height=%d, '
        'format=NV12, framerate=%d/1 ! '
        'nvvidconv flip-method=%d ! '
        'video/x-raw, width=%d, height=%d, format=BGRx ! '
        'videoconvert ! '
        'video/x-raw, format=BGR ! '
        'appsink' % (
            *config.CAMERA_CAPTURE_RESOLUTION,
            config.CAMERA_FRAMERATE,
            config.CAMERA_FLIP_METHOD,
            *config.CAMERA_OUTPUT_RESOLUTION,
        )
    )
