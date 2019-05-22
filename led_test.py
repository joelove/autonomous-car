import Jetson.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13, GPIO.OUT)

while True:
    print('HIGH')
    GPIO.output(13, GPIO.HIGH)
    time.sleep(0.5)
    print('LOW')
    GPIO.output(13, GPIO.LOW)
    time.sleep(0.5)
