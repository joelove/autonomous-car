"""
actuator.py
Class to control the motor and servos.
"""

import time

from Adafruit_PCA9685 import PCA9685


class PCA9685:
    """
    PWM motor controler using PCA9685 boards.
    This is used for most RC Cars
    """
    def __init__(self, channel, frequency=60):
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = PCA9685()
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel

    def set_pulse(self, pulse):
        try:
            self.pwm.set_pwm(self.channel, 0, pulse)
        except OSError as err:
            print("Unexpected issue setting PWM (check wires to motor board): {0}".format(err))
