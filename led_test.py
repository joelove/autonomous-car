import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(40, GPIO.OUT)

while True:
    GPIO.output(40, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(40, GPIO.LOW)
    time.sleep(0.5)
