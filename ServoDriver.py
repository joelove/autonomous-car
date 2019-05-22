from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from board import SCL, SDA

import busio
import config
import signal


class ServoDriver:
    def __init__(self):
        i2c = busio.I2C(SCL, SDA)

        pca = PCA9685(i2c)
        pca.frequency = 60

        self.throttle_servo = servo.ContinuousServo(pca.channels[config.THROTTLE_CHANNEL],
            min_pulse=config.THROTTLE_MIN_PULSE,
            max_pulse=config.THROTTLE_MAX_PULSE)

        self.steering_servo = servo.Servo(pca.channels[config.STEERING_CHANNEL],
            min_pulse=config.STEERING_MIN_PULSE,
            max_pulse=config.STEERING_MAX_PULSE)

        signal.signal(signal.SIGINT, self.handle_sigint)


    def handle_sigint(self, signal, frame):
        print('HANDLE', signal)
        self.reset()


    def set_angle(self, angle):
        print('ANGLE', angle)
        self.steering_servo.angle = angle


    def set_throttle(self, throttle):
        print('THROTTLE', throttle)
        self.throttle_servo.throttle = throttle


    def reset(self):
        print('RESET')
        self.throttle_servo.deinit()
        self.steering_servo.angle = None
