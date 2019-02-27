# BCD7SegmentDisplay.py
#
# Description:
# Implements a counter that is displayed on a common anode 7-segment display
# driven through a BCD To 7-Segment Decoder/Driver (74LS47) IC.  The count is
# reset to 0 when a button is pressed.
#
# Circuit:
# Momentary push button connected to BCM pin 5, physical pin 29.
# Common anode 7-segment display connected through 74LS47 IC to BCM pins 22-25,
# physical pins 15, 16, 18, 22.
#
# Created by John Woolsey on 02/16/2019.
# Copyright (c) 2019 Woolsey Workshop.  All rights reserved.


# Imports
import RPi.GPIO as GPIO
from time import sleep


# Pin Definitions
button =  5  # momentary push button, fires interrupt service routine
bcdA   = 22  # binary coded decimal (BCD) least significant bit (LSB) for 74LS47 A input pin
bcdB   = 23
bcdC   = 24
bcdD   = 25  # binary coded decimal (BCD) most significant bit (MSB) for 74LS47 D input pin


# Global Variables
count = 0  # display counter


# Functions

# Reads a bit of a number
def bitRead(value, bit):
   return value & (1 << bit)  # shift mask to bit position and AND to value

# Resets counter and display to 0
def resetCount(button):
   global count     # declare count as global variable
   count = 0        # reset counter
   displayWrite(0)  # reset display

# Writes value to display using binary coded decimal
def displayWrite(value):
   GPIO.output(bcdA, bitRead(value, 0))  # BCD LSB
   GPIO.output(bcdB, bitRead(value, 1))
   GPIO.output(bcdC, bitRead(value, 2))
   GPIO.output(bcdD, bitRead(value, 3))  # BCD MSB


# Main

# Pin configuration
GPIO.setmode(GPIO.BCM)                                 # use BCM pin numbering
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # utilize microprocessor's internal pull-up resistor
GPIO.setup(bcdA, GPIO.OUT)
GPIO.setup(bcdB, GPIO.OUT)
GPIO.setup(bcdC, GPIO.OUT)
GPIO.setup(bcdD, GPIO.OUT)

# Initialize interrupt service routine
# Calls resetCount() function when button is pressed,
# i.e., the button pin value falls from high to low.
GPIO.add_event_detect(button, GPIO.FALLING, callback=resetCount, bouncetime=250)

# Display count on 7-segment display
print("Press CTRL-C to exit.")
try:
   while True:
      displayWrite(count)        # update display
      count += 1                 # increment counter
      if count == 10: count = 0  # reset to 0 if count exceeds 9
      sleep(1)                   # wait one second

# Cleanup
finally:           # exit cleanly when CTRL+C is pressed
   GPIO.cleanup()  # release all GPIO resources
   print("\nCompleted cleanup of GPIO resources.")
