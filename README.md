# futurice-london-donkey-car

## A Python script to be run on a Raspberry Pi for piloting an autonomous car

This code has been developed and tested on a Raspberry Pi 3 Model B+ running [NOOBS](https://www.raspberrypi.org/downloads/noobs/). Available from the [Raspberry Pi](https://www.raspberrypi.org/) shop:

> https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/

### Installation steps

#### Prerequisites

This project is designed to run on Python v3.5.3, which comes bundled with Raspbian but isn't the default. The easiest way I have found to remedy this quickly and reliably is with this psuedo-hack:

```bash
sudo rm /usr/bin/python
sudo rm /usr/bin/pip

sudo ln -s /usr/bin/python3.5 /usr/bin/python
sudo ln -s /usr/bin/pip3.5 /usr/bin/pip
```

> You probably shouldn't do this, ever. Sue me.

Confirm your python version is 3.5.3 with:

```bash
python --version
```

Also, before we start with the real stuff. I've found that installing the entire dependency tree using Poetry or Pip can take a _**very**_ long time. The problem seems to be London office network specific and seems to be solved by disabling IPv6.

Whilst not completely necessary, I wholeheartedly recommend you add these lines to `/etc/sysctl.conf`:

```bash
sysctl.conf.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
net.ipv6.conf.eth0.disable_ipv6 = 1
net.ipv6.conf.[interface].disable_ipv6 = 1
```

Updating the `apt-get` configuration to explicitly use IPv4 may also help:

```bash
sudo apt-get -o Acquire::ForceIPv4=true update
sudo apt-get -o Acquire::ForceIPv4=true -y dist-upgrade
```

Then reboot:
```bash
sudo reboot
```

Okay, let's get on with the actual installation.

#### Installing dependencies

First let's install things that can't be handled by our package manager:

```bash
sudo apt-get update -y \
&& sudo apt-get install libcblas-dev -y \
&& sudo apt-get install libhdf5-dev -y \
&& sudo apt-get install libhdf5-serial-dev -y \
&& sudo apt-get install libatlas-base-dev -y \
&& sudo apt-get install libjasper-dev -y \
&& sudo apt-get install libqtgui4 -y \
&& sudo apt-get install libqt4-test -y \
&& sudo apt-get install xboxdrv -y \
&& sudo apt-get install joystick -y \
&& sudo apt-get install python-smbus -y \
&& sudo apt-get install i2c-tools -y
```

This project uses [Poetry](https://poetry.eustace.io/) to make package and dependency management easier. Installation instructions can be found in the documentation:

> https://poetry.eustace.io/docs/#installation

Too lazy to actually look at the documentation?

```bash
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

Once we have it, all the PyPI packages should be installed automatically if we run:

```bash
poetry install
```

All sorted? No errors? No, I didn't think so.

This is the bit where you fight with Raspbian, Python and PyPI for four hours before giving up and sending an angry email to Linus Torvalds containing a picture of your genitals.

Works now? Good.

#### Connecting a controller

##### Disable ERTM

```bash
sudo touch /etc/modprobe.d/bluetooth.conf
sudo echo "options bluetooth disable_ertm=Y" >> /etc/modprobe.d/bluetooth.conf
sudo reboot
```

##### Connect using Bluetooth

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

##### Testing the connected controller

```bash
sudo jstest /dev/input/js0
```

### Starting the vehicle

```bash
poetry run python start.py --help
```
---

[![Sponsored](https://img.shields.io/badge/chilicorn-sponsored-brightgreen.svg?logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAPCAMAAADjyg5GAAABqlBMVEUAAAAzmTM3pEn%2FSTGhVSY4ZD43STdOXk5lSGAyhz41iz8xkz2HUCWFFhTFFRUzZDvbIB00Zzoyfj9zlHY0ZzmMfY0ydT0zjj92l3qjeR3dNSkoZp4ykEAzjT8ylUBlgj0yiT0ymECkwKjWqAyjuqcghpUykD%2BUQCKoQyAHb%2BgylkAyl0EynkEzmkA0mUA3mj86oUg7oUo8n0k%2FS%2Bw%2Fo0xBnE5BpU9Br0ZKo1ZLmFZOjEhesGljuzllqW50tH14aS14qm17mX9%2Bx4GAgUCEx02JySqOvpSXvI%2BYvp2orqmpzeGrQh%2Bsr6yssa2ttK6v0bKxMBy01bm4zLu5yry7yb29x77BzMPCxsLEzMXFxsXGx8fI3PLJ08vKysrKy8rL2s3MzczOH8LR0dHW19bX19fZ2dna2trc3Nzd3d3d3t3f39%2FgtZTg4ODi4uLj4%2BPlGxLl5eXm5ubnRzPn5%2Bfo6Ojp6enqfmzq6urr6%2Bvt7e3t7u3uDwvugwbu7u7v6Obv8fDz8%2FP09PT2igP29vb4%2BPj6y376%2Bu%2F7%2Bfv9%2Ff39%2Fv3%2BkAH%2FAwf%2FtwD%2F9wCyh1KfAAAAKXRSTlMABQ4VGykqLjVCTVNgdXuHj5Kaq62vt77ExNPX2%2Bju8vX6%2Bvr7%2FP7%2B%2FiiUMfUAAADTSURBVAjXBcFRTsIwHAfgX%2FtvOyjdYDUsRkFjTIwkPvjiOTyX9%2FAIJt7BF570BopEdHOOstHS%2BX0s439RGwnfuB5gSFOZAgDqjQOBivtGkCc7j%2B2e8XNzefWSu%2BsZUD1QfoTq0y6mZsUSvIkRoGYnHu6Yc63pDCjiSNE2kYLdCUAWVmK4zsxzO%2BQQFxNs5b479NHXopkbWX9U3PAwWAVSY%2FpZf1udQ7rfUpQ1CzurDPpwo16Ff2cMWjuFHX9qCV0Y0Ok4Jvh63IABUNnktl%2B6sgP%2BARIxSrT%2FMhLlAAAAAElFTkSuQmCC)](http://spiceprogram.org/oss-sponsorship)
