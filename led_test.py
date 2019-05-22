from adafruit_pca9685 import PCA9685
from board import SCL, SDA

import busio


i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)
pca.frequency = 60

led_channel = pca.channels[8]
led_channel.duty_cycle = 0xffff
