import Jetson.GPIO as GPIO
import time

channel = 13
frequency = 50

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(channel, GPIO.OUT)

white_led = GPIO.PWM(channel, frequency)

while True:
    print('HIGH')
    white_led.ChangeDutyCycle(1)
    time.sleep(0.5)
    print('LOW')
    white_led.ChangeDutyCycle(0)
    time.sleep(0.5)
