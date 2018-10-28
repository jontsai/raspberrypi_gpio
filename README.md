Raspberry Pi GPIO
=================

A collection of scripts and such for playing with Raspberry Pi GPIO

Some of my personal tinkering/hack projects, will get more organized later.

Setup and Installation
======================

0. Make sure you have the prerequisite packages and environment installed for Raspbian, check out my other repository of scripts on GitHub:  
   https://github.com/jontsai/raspbian-bootstrap
1. Clone this repository  
   `git clone git@github.com:jontsai/raspberrypi_gpio`
2. Create a `virtualenv` for local testing  
   `virtualenv venv`
   `venv/bin/pip install -R requirements.txt`
3. Check out the `demo/` or `tutorial/`

Demo
====
See `demo/` subdirectory

Raspberry Pi GPIO Pin layout
============================
    RPi.GPIO    Raspberry Pi Name
    1           3V3
    2           5V0
    3           SDA0
    4           DNC
    5           SCL0
    6           GND
    7           GPIO7*
    8           TXD
    9           DNC
    10          RXD
    11          GPIO0*
    12          GPIO1*
    13          GPIO2*
    14          DNC
    15          GPIO3*
    16          GPIO4*
    17          DNC
    18          GPIO5*
    19          SPI_MOSI
    20          DNC
    21          SPI_MISO
    22          GPIO6*
    23          SPI_SCLK
    24          SPI_CE0_N
    25          DNC
    26          SPI_CE1_N
