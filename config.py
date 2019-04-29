"""
CAR CONFIG

This file is read by your car application's manage.py script to change the car
performance.

EXAMPLE
-----------
import dk
cfg = dk.load_config('config.py')
print(cfg.CAMERA_RESOLUTION)
"""

import os

#PATHS
CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))

DATA_PATH = os.path.join(CAR_PATH, 'data')
MODELS_PATH = os.path.join(CAR_PATH, 'models')
TUB_PATH = os.path.join(CAR_PATH, 'tub')

#VEHICLE
DRIVE_LOOP_HZ = 10
MAX_LOOPS = 100000

#CAMERA
CAMERA_RESOLUTION = (640, 480)
CAMERA_FRAMERATE = DRIVE_LOOP_HZ

#STEERING
STEERING_CHANNEL = 1
STEERING_LEFT_PWM = 280
STEERING_RIGHT_PWM = 450
STEERING_RANGE = 100

#THROTTLE
THROTTLE_CHANNEL = 0
THROTTLE_FORWARD_PWM = 390
THROTTLE_STOPPED_PWM = 380
THROTTLE_REVERSE_PWM = 360
CRUISING_MODE_THROTTLE = 0
THROTTLE_MIN = 0.25
THROTTLE_MAX = 0.5

#TRAINING
BATCH_SIZE = 128
TRAIN_TEST_SPLIT = 0.8

#JOYSTICK
USE_JOYSTICK_AS_DEFAULT = False
JOYSTICK_MAX_THROTTLE = 1.0
JOYSTICK_STEERING_SCALE = 1.0
AUTO_RECORD_ON_THROTTLE = True

#ROPE.DONKEYCAR.COM
ROPE_TOKEN='ROPE_TOKEN'
