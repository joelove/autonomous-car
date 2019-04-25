import config

from servo_driver import ServoDriver


class Auto:
    def drive(self):
        print('>> Autonomous driving <<')

        servos = ServoDriver()

        while True:
            servos.set_throttle(config.THROTTLE_MAX) # trololololol
