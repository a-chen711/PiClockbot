#!/bin/sh
# launcher.sh
# Launcher shell to run the python code at startup for the Raspberry Pi

cd /
cd home/pi/bcm2835-1.60/LCD_Module_code/LCD_Module_RPI_code/RaspberryPi/python/example
python3 PiClock_Tele.py
cd /