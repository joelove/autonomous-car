import sys
import config

from Camera import Camera
from ServoDriver import ServoDriver


class Vehicle:
    def __init__(self):
        self.camera = Camera()
        self.servos = ServoDriver()


    def axis_to_unit_interval(self, axis):
        return (axis + 1) / 2


    def number_to_exponential(self, axis):
        return axis ** 3


    def steering_axis_to_interval(self, axis):
        steering_exponential_axis = self.number_to_exponential(axis)

        return steering_exponential_axis


    def throttle_axis_to_interval(self, axis):
        throttle_interval = self.axis_to_unit_interval(axis)
        throttle_exponential_interval = self.number_to_exponential(throttle_interval)

        return throttle_exponential_interval


    def interval_to_steering_angle(self, interval):
        unit_interval = self.axis_to_unit_interval(interval)
        actual_angle = unit_interval * config.STEERING_RANGE_DEGREES
        actuation_range = self.servos.steering_servo.actuation_range
        range_difference = actuation_range - config.STEERING_RANGE_DEGREES
        steering_lead = range_difference / 2
        steering_angle = actuation_range - steering_lead - actual_angle

        return steering_angle


    def interval_to_throttle(self, interval):
        if not interval:
            return interval

        throttle_range = config.THROTTLE_MAX_PERCENT - config.THROTTLE_MIN_PERCENT
        throttle_percent = config.THROTTLE_MIN_PERCENT + interval * throttle_range
        throttle = throttle_percent / 100

        return throttle

    def end(self):
        self.servos.reset_all()
        sys.exit(0)
