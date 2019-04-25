import config

from controller import Controller
from servo_driver import ServoDriver


class Manual:
    def __init__(self, **kwargs):
        self.capture = kwargs["capture"]


    def axis_to_unit_interval(self, range):
        return (range + 1) / 2


    def axis_to_angle(self, axis):
        interval = self.axis_to_unit_interval(axis)
        angle = interval * config.STEERING_RANGE

        return angle


    def axis_to_throttle(self, axis):
        interval = self.axis_to_unit_interval(axis)
        throttle = interval * config.THROTTLE_MAX

        return throttle


    def process_controller_state(self, controller_state):
        axis_states, button_states = controller_state

        angle = self.axis_to_angle(axis_states["x"])
        throttle = self.axis_to_throttle(axis_states["gas"])

        print(angle)
        print(throttle)

        servos = ServoDriver()
        servos.set_angle(angle)
        servos.set_throttle(throttle)


    def drive(self):
        print('>> Manual driving <<')
        print('Data capture: ' + str(self.capture))

        controller = Controller()
        controller.read(self.process_controller_state)
