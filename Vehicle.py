import config
import cv2
import signal
import sys

from ServoDriver import ServoDriver
from utilities.stream_pipelines import gstreamer_pipeline


class Vehicle:
    def __init__(self):
        signal.signal(signal.SIGINT, self.handle_sigint)

        self.camera = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        self.servos = ServoDriver()


    def handle_sigint(self, signal, frame):
        self.servos.reset_servos()
        self.camera.release()

        sys.exit(0)


    def axis_to_unit_interval(self, axis):
        return (axis + 1) / 2


    def interval_to_inverse(self, interval):
        return -interval


    def number_to_exponential(self, axis):
        return axis ** 3


    def steering_axis_to_interval(self, axis):
        steering_exponential_interval = self.number_to_exponential(axis)
        inverse_interval = self.interval_to_inverse(steering_exponential_interval)

        return inverse_interval


    def throttle_axis_to_interval(self, axis):
        throttle_interval = self.axis_to_unit_interval(axis)
        throttle_exponential_interval = self.number_to_exponential(throttle_interval)
        throttle_inverse = self.interval_to_inverse(throttle_exponential_interval)

        return throttle_inverse + config.THROTTLE_SHIFT


    def interval_to_steering_angle(self, interval):
        unit_interval = self.axis_to_unit_interval(interval)
        actual_angle = unit_interval * config.STEERING_RANGE_DEGREES
        actuation_range = self.servos.steering_servo.actuation_range
        range_difference = actuation_range - config.STEERING_RANGE_DEGREES
        steering_lead = range_difference / 2
        steering_angle = actuation_range - steering_lead - actual_angle

        return steering_angle


    def interval_to_throttle(self, interval):
        if not interval < config.THROTTLE_SHIFT:
            return interval

        throttle_range = config.THROTTLE_MAX_PERCENT - config.THROTTLE_MIN_PERCENT
        throttle_percent = config.THROTTLE_MIN_PERCENT + interval * throttle_range
        throttle = throttle_percent / 100

        return throttle
