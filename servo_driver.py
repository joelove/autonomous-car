import config

from adafruit_servokit import ServoKit


class ServoDriver:
    def __init__(self, channels=16):
        kit = ServoKit(channels=channels)
        self.steering_servo = kit.servo[config.STEERING_CHANNEL]
        self.throttle_servo = kit.servo[config.THROTTLE_CHANNEL]

    def set_angle(self, angle):
        self.steering_servo.angle = angle

    def set_throttle(self, throttle):
        self.throttle_servo.throttle = throttle
