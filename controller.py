import time

from joystick import Joystick


SAMPLE_FREQUENCY = 10
TICK_LENGTH = 1.0 / SAMPLE_FREQUENCY


def handle_steering(joystick):
    angle = joystick.leftX()
    print('Angle: ' + str(angle))


def handle_throttle(joystick):
    throttle = joystick.rightTrigger()
    print('Throttle: ' + str(throttle))


def read_controller():
    joystick = Joystick()

    while not joystick.Back():
        start_time = time.time()

        if joystick.connected():
            handle_steering(joystick)
            handle_throttle(joystick)

        time.sleep(TICK_LENGTH - ((time.time() - start_time) % TICK_LENGTH))

    joystick.close()

# if joystick.Back(): handle_back(joystick)
# if joystick.A(): handle_a(joystick)
# if joystick.B(): handle_b(joystick)
# if joystick.X(): handle_x(joystick)
# if joystick.Y(): handle_y(joystick)
# if joystick.dpadUp(): handle_dpadUp(joystick)
# if joystick.dpadDown(): handle_dpadDown(joystick)
# if joystick.dpadLeft(): handle_dpadLeft(joystick)
# if joystick.dpadRight(): handle_dpadRight(joystick)
