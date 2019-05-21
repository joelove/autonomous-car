from ServoDriver import ServoDriver

servos = ServoDriver()

try:
    while True:
        raw_value = input("Enter speed: ")
        servo_value = int(raw_value)
        servos.set_throttle(servo_value)
except KeyboardInterrupt:
    pass
