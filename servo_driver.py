import config

from adafruit_servokit import ServoKit


class ServoDriver:
    range = 180.0

    def __init__(self, channels=16):
        kit = ServoKit(channels=channels)
        self.throttle_servo = kit.continuous_servo[config.THROTTLE_CHANNEL]
        self.steering_servo = kit.servo[config.STEERING_CHANNEL]
        self.steering_servo.set_pulse_width_range(config.STEERING_LEFT_PWM,
                                                  config.STEERING_RIGHT_PWM)

    def set_angle(self, angle):
        self.steering_servo.angle = angle

    def set_throttle(self, throttle):
        self.throttle_servo.throttle = throttle
