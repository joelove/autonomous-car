import config

from controller import Controller
from servo_driver import ServoDriver


def axis_to_unit_interval(range):
    return (range + 1) / 2


def axis_to_angle(axis):
    interval = axis_to_unit_interval(axis)
    angle = interval * config.STEERING_RANGE

    return angle


def axis_to_throttle(axis):
    interval = axis_to_unit_interval(axis)
    throttle = interval * config.THROTTLE_MAX

    return throttle


def process_controller_state(controller_state):
    axis_states, button_states = controller_state

    angle = axis_to_angle(axis_states['x'])
    throttle = axis_to_throttle(axis_states['gas'])

    print(angle)
    print(throttle)

    servos = ServoDriver()
    servos.set_angle(angle)
    servos.set_throttle(throttle)


def start():
    controller = Controller()
    controller.read(process_controller_state)


if __name__ == '__main__':
    start()
