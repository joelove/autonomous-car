# futurice-london-donkey-car

## A Python script to be run on a Raspberry Pi for piloting an autonomous car

This code has been developed and tested on a Raspberry Pi 3 Model B+ running [NOOBS](https://www.raspberrypi.org/downloads/noobs/). Available from the [Raspberry Pi](https://www.raspberrypi.org/) shop:

> https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/

### Installation steps

#### Prerequisites

Before we start with the real stuff, I've found that network connections from the Raspberry Pi can hang for a long time during initialization, causing multiple dependency installations to take a _very_ long time. The problem seems to be London office network specific and is solved by disabling IPv6.

Whilst not completely necessary, I wholeheartedly recommend you modify the system configuration file to explicitly disable IPv6:

```bash
sudo echo 'sysctl.conf.ipv6.conf.all.disable_ipv6 = 1' >> /etc/sysctl.conf
sudo echo 'net.ipv6.conf.default.disable_ipv6 = 1' >> /etc/sysctl.conf
sudo echo 'net.ipv6.conf.lo.disable_ipv6 = 1' >> /etc/sysctl.conf
sudo echo 'net.ipv6.conf.eth0.disable_ipv6 = 1' >> /etc/sysctl.conf
sudo echo 'net.ipv6.conf.[interface].disable_ipv6 = 1' >> /etc/sysctl.conf
```

Updating the `apt-get` configuration to force IPv4 may also help:

```bash
sudo apt-get -o Acquire::ForceIPv4=true update
sudo apt-get -o Acquire::ForceIPv4=true -y dist-upgrade
```

Then reboot:
```bash
sudo reboot
```

Once that's done, confirm the Advanced Package Tool is up to date:

```bash
sudo apt-get update -y
```

#### Python

This project is designed to run on Python 3, which comes bundled with Raspbian but isn't the default or even the latest version.

Rather than mess with the preinstalled versions by adding aliases or symbolic links, let's just handle Python versions using [pyenv](https://github.com/pyenv/pyenv). Ruby developers will recognise this tool as a port of rbenv.

```bash
sudo apt-get install bzip2 libbz2-dev libreadline6 libreadline6-dev libffi-dev libssl1.0-dev sqlite3 libsqlite3-dev -y
```
```bash
git clone git://github.com/yyuu/pyenv.git ~/.pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

exec $SHELL
```

Installing and switching versions with pyenv is as simple as:

```bash
pyenv install 3.7.3
pyenv global 3.7.3
```

Confirm your current python version with:

```bash
python --version
```

Okay, let's get on with the actual installation.

#### Installing dependencies

First let's install things that can't be handled by the Python package manager:

```bash
sudo apt-get install libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test xboxdrv joystick python-smbus i2c-tools -y
```

This project uses [Poetry](https://poetry.eustace.io/) to make package and dependency management easier:

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
sudo echo 'options bluetooth disable_ertm=Y' >> /etc/modprobe.d/bluetooth.conf
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
