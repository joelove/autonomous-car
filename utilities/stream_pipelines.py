import os
import sys

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
root_dir = os.path.join(script_dir, os.pardir)

sys.path.append(root_dir)

import config


def gstreamer_pipeline ():
    print((
        *config.CAMERA_RESOLUTION,
        config.CAMERA_FRAMERATE,
        config.CAMERA_FLIP_METHOD,
        *config.CAMERA_RESOLUTION,
    ))
    
    return (
        'nvarguscamerasrc ! '
        'video/x-raw(memory:NVMM), '
        'width=(int)%d, height=(int)%d, '
        'format=(string)NV12, framerate=(fraction)%d/1 ! '
        'nvvidconv flip-method=%d ! '
        'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
        'videoconvert ! '
        'video/x-raw, format=(string)BGR ! appsink'  % (
            *config.CAMERA_RESOLUTION,
            config.CAMERA_FRAMERATE,
            config.CAMERA_FLIP_METHOD,
            *config.CAMERA_RESOLUTION,
        )
    )
