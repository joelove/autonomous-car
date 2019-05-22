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
        self.enable_leds()


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


    def enable_led(self, channel):
        print('ENABLE', channel)
        self.pca.channels[channel].duty_cycle = 0xffff


    def enable_leds(self):
        map(self.enable_led, config.RED_LED_CHANNELS)
        map(self.enable_led, config.WHITE_LED_CHANNELS)


    def handle_sigint(self, signal, frame):
        self.reset()
        sys.exit(0)


    def set_angle(self, angle):
        self.steering_servo.angle = angle


    def set_throttle(self, throttle):
        self.throttle_servo.throttle = throttle


    def reset(self):
        self.throttle_servo.deinit()
        self.steering_servo.angle = None
