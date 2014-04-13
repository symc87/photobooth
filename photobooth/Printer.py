#!/usr/bin/python

from Modules.ThermalPrinter import Adafruit_Thermal
import Image,time

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

printer.wake()

# Barcode examples
printer.setDefault() # Restore printer to defaults

printer.feed(1)
image=Image.open("test.jpg")
bbox=image.getbbox()
if bbox[2] > 384:
    image=image.crop(((bbox[2]/2)-(bbox[3]/2),0,(bbox[2]/2)+(bbox[3]/2),bbox[3]))
    image=image.resize((384,384))
for i in range(4):
    printer.sleep()      # Tell printer to sleep
    time.sleep(1)
    printer.wake()
    printer.printImage(image, True)

#printer.printBitmap(adalogo.width, adalogo.height, adalogo.data)

    printer.feed(1)

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
    