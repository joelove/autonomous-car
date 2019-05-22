from adafruit_pca9685 import PCA9685
from board import SCL, SDA

import busio
import time


i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)
pca.frequency = 60

RED_LED_CHANNEL = 8
WHITE_LED_CHANNEL = 9

red_led = pca.channels[RED_LED_CHANNEL]
white_led = pca.channels[WHITE_LED_CHANNEL]

while True:
    red_led.duty_cycle = 0xffff
    time.sleep(0.25)
    white_led.duty_cycle = 0xffff
    time.sleep(0.25)
    red_led.duty_cycle = 0
    time.sleep(0.25)
    white_led.duty_cycle = 0
    time.sleep(0.25)
