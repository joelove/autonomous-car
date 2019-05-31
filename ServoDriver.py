from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from board import SCL, SDA

import busio
import config
import signal
import sys

from adafruit_pca9685 import PCA9685
from board import SCL, SDA


class ServoDriver:
    def __init__(self):
        signal.signal(signal.SIGINT, self.handle_sigint)

        self.initialize_pca()
        self.initialize_servos()

        self.enable_lights()


    def handle_sigint(self, signal, frame):
        self.reset_servos()
        sys.exit(0)


    def initialize_pca(self):
        i2c = busio.I2C(SCL, SDA)

        self.pca = PCA9685(i2c)
        self.pca.frequency = 60


    def initialize_servos(self):
        throttle_channel = self.pca.channels[config.THROTTLE_CHANNEL]
        steering_channel = self.pca.channels[config.STEERING_CHANNEL]

        self.throttle_servo = servo.ContinuousServo(throttle_channel,
            min_pulse=config.THROTTLE_MIN_PULSE,
            max_pulse=config.THROTTLE_MAX_PULSE)

        self.steering_servo = servo.Servo(steering_channel,
            min_pulse=config.STEERING_MIN_PULSE,
            max_pulse=config.STEERING_MAX_PULSE)


    def reset_servos(self):
        self.throttle_servo.throttle = config.THROTTLE_SHIFT
        self.steering_servo.angle = None


    def set_angle(self, angle):
        self.steering_servo.angle = angle
        self.set_indicators(angle)


    def set_throttle(self, throttle):
        self.throttle_servo.throttle = throttle


    def enable_led(self, channel):
        self.pca.channels[channel].duty_cycle = 0xffff


    def disable_led(self, channel):
        self.pca.channels[channel].duty_cycle = 0


    def enable_lights(self):
        for channel in config.HEAD_LIGHT_CHANNELS:
            self.enable_led(channel)

        for channel in config.REAR_LIGHT_CHANNELS:
            self.enable_led(channel)


    def disable_indicators(self):
        self.disable_led(config.LEFT_INDICATOR_CHANNEL)
        self.disable_led(config.RIGHT_INDICATOR_CHANNEL)


    def enable_indicator(self, angle):
        positive_steering_angle = angle > 0

        if positive_steering_angle:
            self.enable_led(config.LEFT_INDICATOR_CHANNEL)
        else:
            self.enable_led(config.RIGHT_INDICATOR_CHANNEL)


    def set_indicators(self, angle):
        if not angle:
            self.disable_indicators()

        self.enable_indicator(angle)
