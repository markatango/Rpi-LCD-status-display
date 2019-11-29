# Rpi-LCD-status-display

Displays network and hostname information on adapitft LCD display.  

## Behavior
If the IoT node acquires an IP address, then the LCD background color is GREEN and displays the IPv4 network address (CIDR), IPv4 host address, and hostname.  If the IoT node fails to acquire an IP address, then the LCD background color is RED.

<img src="https://github.com/miyachiamericaeurope/amya-status-display/blob/media/NoConnection.jpg" alt="No connection" width="320p" height="240"> <img src="https://github.com/miyachiamericaeurope/amya-status-display/blob/media/Connection.jpg" alt="OK connection" width="320p" height="240">


## Installation

### Create image:
1) Burn Raspbian Buster Lite onto microSD card
2) `touch ssh.txt`
3) Copy these files into `/boot`:

  `bootfiles/cmdline.txt`
  `bootfiles/config.txt`
  `bootfiles/adafruit-pitft.sh`
  
4) Install microSD card into IoT node and apply power. Boot up process takes a few minutes; wait until login prompt appears
5) Confirm the device is reachable via `ssh` using default Raspberry pi username and password.

### Install Pillow:
6) From provisioning server, ssh to <default_username>@<Iot_node_IP>
7) Install pre-requisite software into IoT node:

(Reference: https://www.techcoil.com/blog/how-to-setup-python-imaging-library-pillow-on-raspbian-stretch-lite-for-processing-images-on-your-raspberry-pi/)

(note: this procedure also works for Raspbian Buster Lite)
```
sudo apt-get update
sudo apt-get install libjpeg-dev -y
sudo apt-get install zlib1g-dev -y
sudo apt-get install libfreetype6-dev -y
sudo apt-get install liblcms1-dev -y
sudo apt-get install libopenjp2-7 -y
sudo apt-get install libtiff5 -y
sudo pip install pillow
```
### Clone this repo into `/opt`
8) `cd /opt`
9) `sudo git clone https://github.com/markatango/Rpi-LCD-status-display.git`

### Configure LCD screen
10) `sudo /boot/adafruit-pitft.sh`
11) Answer questions as follows:
```
  Select configuration:
  1. PiTFT 2.4", 2.8" or 3.2" resistive (240x320)
  ...

  SELECT 1-5: 1 

  Select rotation:
  1. 90 degrees (landscape)
  ...

  SELECT 1-4: 1
  ```
  Lots of stuff happens....
  ```
  Would you like the console to appear on the PiTFT display? [y/n]  n

  Would you like the HDMI display to mirror to the PiTFT display? [y/n] y
  ```

This script installs additional `apt` and `pip` packages, and modifies `cmdline.txt` and `config.txt`.

1123) Reboot system at prompt

### Install service
13) `sudo cp rpi-logo-2.service /etc/systemd/system`
14) `sudo systemctl enable rpi-logo-2`
15) `sudo systemctl start rpi-logo-2`

