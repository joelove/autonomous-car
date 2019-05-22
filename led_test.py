from adafruit_pca9685 import PCA9685
from board import SCL, SDA

import busio
import time


i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)
pca.frequency = 60

led_channel = pca.channels[8]

while True:
    print('ON')
    led_channel.duty_cycle = 0xffff
    time.sleep(0.5)
    print('OFF')
    led_channel.duty_cycle = 0
    time.sleep(0.5)
