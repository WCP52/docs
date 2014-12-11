#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import sys
import time

def getline (s):
    return s.readline ().decode ('ascii').strip ()

def printline (s, indent=2):
    """Print a line from serial, indented."""
    line = getline (s)
    print ((" " * indent) + line)
    return line

# Connect
print ("Connecting to GPA...")
s = serial.Serial ("/dev/ttyACM0", 115200, timeout=1)

# Initialize
print ("Initializing microcontroller...")
s.write (b"*RST\r\n")
s.read (100)
s.write (b"*IDN?\r\n")
print ("  OK")
print ("  identity string = " + s.readline ().decode ('ascii').strip ())

print ("Initializing synthesizer...")
s.write (b"T:INIF\r\n")
time.sleep (0.5)
s.write (b"T:INCK\r\n")
time.sleep (0.5)
print ("  OK")

print ("Initializing frontend... ")
s.write (b"T:FREQ 0, 0\r\n")
printline (s)
s.write (b"T:AMP 0, 0\r\n")
printline (s)
s.write (b"T:CH 1\r\n")
time.sleep (0.5)
print ("  OK")

print ("Collecting phase data...")
freq = 10e3
s.write (("T:FREQ 1, %f\r\n" % freq).encode ('ascii'))
getline (s)
s.write (("T:FREQ 0, %f\r\n" % freq).encode ('ascii'))
getline (s)
s.write (b"T:AMP 1, 0.5\r\n")
getline (s)
s.write (b"T:AMP 0, 0.5\r\n")
getline (s)

phases = []
data = []
for phase in range (0, 360, 4):
    s.write (("T:PHASE 0, %f\r\n" % phase).encode ('ascii'))
    getline (s)
    s.write (b"T:SAM 5000\r\n")
    level = float (getline (s))
    phases.append (phase)
    data.append (level)
    print (phase, level)

plot, = plt.plot (phases, data)
plt.xlabel ("Phase (deg)")
plt.ylabel ("Amplitude, raw")
plt.title ("Phase Shift, uncalibrated")
plt.grid (True)

plt.draw ()
plt.waitforbuttonpress (-1)


s.write (b"T:AMP 1, 0\r\n")
getline (s)
s.write (b"T:AMP 0, 0\r\n")
getline (s)
