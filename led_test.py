import Jetson.GPIO as GPIO
import time

channel = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.OUT)

while True:
    print('HIGH')
    GPIO.output(channel, GPIO.HIGH)
    time.sleep(0.5)
    print('LOW')
    GPIO.output(channel, GPIO.LOW)
    time.sleep(0.5)
