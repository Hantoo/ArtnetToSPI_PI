#!/usr/bin/python

#Requirements
#pip install rpi-tlc59711
#pip install stupidArtnet

#______________________________________________________________
#| NAME   | RPI Pin | RPi GPIO | TLC59711 | AdaFruit TLC59711 |
#|________|_________|__________|__________|___________________|
#| Data   |    18   |  GPIO24  |   SDTI   |        DI         |
#| Clock  |    16   |  GPIO23  |   SCKI   |        CI         |
#| 3v3    |     1   |  3v3     |   3v3    |        VCC        |
#| Ground |     6   |  GND     |   GND    |        GND        |
#|________|_________|__________|__________|___________________|    

# 0xFFFF = 100%
# 0x7FFF = 50%
# 0x3FFF = 25%
# 0x0000 = 0%

import RPi.GPIO as GPIO
#from tlc59711.tlc59711 import tlc59711
from stupidArtnet import StupidArtnetServer
import time

from rpi_ws281x import PixelStrip, Color
import argparse

# LED strip configuration:
LED_COUNT = 160       # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

TW_LED_PIN = 21          # GPIO pin connected to the pixels (18 uses PWM!).

RGBstrip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
RGBstrip.begin()

TWstrip = PixelStrip(LED_COUNT, TW_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
TWstrip.begin()

def artnetUpdateU1(data):
	#print("Data Universe 1")
	for dataIdx in range(int(len(data)/3)):
		RGBstrip.setPixelColorRGB(dataIdx,int(data[(dataIdx*3)+0]),int(data[(dataIdx*3)+2]),int(data[(dataIdx*3)+1]))
	RGBstrip.show()
		#tlc.SetPWM(dataIdx, pow(data[dataIdx],2))
	

def artnetUpdateU2(data):
	for dataIdx in range(int(len(data)/3)):
		TWstrip.setPixelColorRGB(dataIdx,int(data[(dataIdx*3)+0]),int(data[(dataIdx*3)+2]),int(data[(dataIdx*3)+1]))
	TWstrip.show()
	





#print("Setting GPIO Pins")
#GPIO.setmode(GPIO.BCM)
#tlc = tlc59711(23, 24)

print("Setting Artnet Input")
a = StupidArtnetServer()

# For every universe we would like to receive,
# add a new listener with a optional callback
# the return is an id for the listener
u1_listener = a.register_listener(1, callback_function=artnetUpdateU1)
u2_listener = a.register_listener(2, callback_function=artnetUpdateU2)



# tlc.SetGlobalBrightness(0x0F)
while(True):
	#a.getbuf
	time.sleep(0.03)
	#tlc.SetLED(chan, 0x0000, 0x0000, 0x0000)

#GPIO.cleanup()