# autonomous-car

## A Python script to be run on a Raspberry Pi for piloting an autonomous car

This code has been developed and tested on a Raspberry Pi 3 Model B+ running [NOOBS](https://www.raspberrypi.org/downloads/noobs/). Available from the [Raspberry Pi](https://www.raspberrypi.org/) shop:

> https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/

### Installation steps

#### Prerequisites

Whilst not completely necessary, I wholeheartedly recommend explicitly disabling IPv6 on the Raspberry Pi by adding these lines to `/etc/sysctl.conf`:

```bash
sysctl.conf.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
net.ipv6.conf.eth0.disable_ipv6 = 1
net.ipv6.conf.[interface].disable_ipv6 = 1
```

This should make network connections significantly quicker to initialise on _some_ networks (most notably, the London Futurice office). Once that's done, reboot:
```bash
sudo reboot
```

Before we install anything, let's confirm the APT is up to date:

```bash
sudo apt-get update -y
```

#### Python

This project is designed to run on Python `3.5.3`, which comes bundled with the latest version of Raspbian (at time of writing) but isn't the default.

We can use Python 3 with the `python3` command:

```bash
python3 --version
```

Other versions might work but finding an ARM-compiled binary for `numpy` that works as intended is entirely contingent on [piwheels](https://www.piwheels.org/) and can be quite a lot of hassle.

#### Installing dependencies

```bash
sudo apt-get install libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test xboxdrv joystick python-smbus i2c-tools -y
```

##### Raspberry Pi

```bash
pip3 install numpy==1.13.3 opencv-python tensorflow picamera adafruit-circuitpython-servokit
```

##### Jetson Nano

```bash
pip3 install adafruit-circuitpython-pca9685 adafruit-circuitpython-motor
```

#### Connecting a controller

Whilst initially configuring the Pi, we need to disable ERTM to allow Bluetooth connections from an Xbox Controller:

```bash
sudo touch /etc/modprobe.d/bluetooth.conf
sudo bash -c "echo 'options bluetooth disable_ertm=Y' >> /etc/modprobe.d/bluetooth.conf"
sudo reboot
```

##### Pairing a new controller

```bash
sudo bluetoothctl
```
```
agent on
default-agent
scan on
connect CONTROLLER_MAC_ADDRESS
trust CONTROLLER_MAC_ADDRESS
exit
```

Once this is done, the controller should attempt to connect to the Pi automatically any time it's turned on until it is manually connected to another device.

##### Connecting to a previously paired controller

If the controller becomes disconnected, we don't need to pair again. We can connect to the controller manually:

```bash
sudo bluetoothctl
```
```
devices
connect CONTROLLER_MAC_ADDRESS
exit
```

If this doesn't work, it might be connected to another device. Plugging the controller in to a PC with micro-USB should clear its existing connection.

##### Testing a connected controller

```bash
sudo jstest /dev/input/js0
```

### Starting the vehicle

```bash
python3 start.py --help
```
---

[![Sponsored](https://img.shields.io/badge/chilicorn-sponsored-brightgreen.svg?logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAPCAMAAADjyg5GAAABqlBMVEUAAAAzmTM3pEn%2FSTGhVSY4ZD43STdOXk5lSGAyhz41iz8xkz2HUCWFFhTFFRUzZDvbIB00Zzoyfj9zlHY0ZzmMfY0ydT0zjj92l3qjeR3dNSkoZp4ykEAzjT8ylUBlgj0yiT0ymECkwKjWqAyjuqcghpUykD%2BUQCKoQyAHb%2BgylkAyl0EynkEzmkA0mUA3mj86oUg7oUo8n0k%2FS%2Bw%2Fo0xBnE5BpU9Br0ZKo1ZLmFZOjEhesGljuzllqW50tH14aS14qm17mX9%2Bx4GAgUCEx02JySqOvpSXvI%2BYvp2orqmpzeGrQh%2Bsr6yssa2ttK6v0bKxMBy01bm4zLu5yry7yb29x77BzMPCxsLEzMXFxsXGx8fI3PLJ08vKysrKy8rL2s3MzczOH8LR0dHW19bX19fZ2dna2trc3Nzd3d3d3t3f39%2FgtZTg4ODi4uLj4%2BPlGxLl5eXm5ubnRzPn5%2Bfo6Ojp6enqfmzq6urr6%2Bvt7e3t7u3uDwvugwbu7u7v6Obv8fDz8%2FP09PT2igP29vb4%2BPj6y376%2Bu%2F7%2Bfv9%2Ff39%2Fv3%2BkAH%2FAwf%2FtwD%2F9wCyh1KfAAAAKXRSTlMABQ4VGykqLjVCTVNgdXuHj5Kaq62vt77ExNPX2%2Bju8vX6%2Bvr7%2FP7%2B%2FiiUMfUAAADTSURBVAjXBcFRTsIwHAfgX%2FtvOyjdYDUsRkFjTIwkPvjiOTyX9%2FAIJt7BF570BopEdHOOstHS%2BX0s439RGwnfuB5gSFOZAgDqjQOBivtGkCc7j%2B2e8XNzefWSu%2BsZUD1QfoTq0y6mZsUSvIkRoGYnHu6Yc63pDCjiSNE2kYLdCUAWVmK4zsxzO%2BQQFxNs5b479NHXopkbWX9U3PAwWAVSY%2FpZf1udQ7rfUpQ1CzurDPpwo16Ff2cMWjuFHX9qCV0Y0Ok4Jvh63IABUNnktl%2B6sgP%2BARIxSrT%2FMhLlAAAAAElFTkSuQmCC)](http://spiceprogram.org/oss-sponsorship)
