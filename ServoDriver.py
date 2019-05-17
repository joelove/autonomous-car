from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from board import SCL, SDA

import busio
import config


class ServoDriver:
    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        pca = PCA9685(i2c)
        pca.frequency = 50

        self.throttle_servo = servo.ContinuousServo(pca.channels[config.THROTTLE_CHANNEL])
        self.steering_servo = servo.Servo(pca.channels[config.STEERING_CHANNEL],
            min_pulse=config.STEERING_MIN_PULSE,
            max_pulse=config.STEERING_MAX_PULSE)

    def set_angle(self, angle):
        self.steering_servo.angle = angle

    def set_throttle(self, throttle):
        self.throttle_servo.throttle = throttle
