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
s.write (b"T:CH 0\r\n")
time.sleep (0.5)
print ("  OK")

print ("Collecting data... ")
freqs = np.logspace(3, 8.1761, 60) # 1 kHz to 150 MHz
data = []
for i in freqs:
    s.write (("T:FREQ 1, %f\r\n" % i).encode ('ascii'))
    getline (s)
    s.write (b"T:SAM 5000\r\n")
    level = float (getline (s))
    db = level / (4095 * 24e-3 / 3.3)
    print ("%.2f Hz\t%.2f dB" % (i, db))
    data.append (db)

data = [i-data[0] for i in data]

plt.ion ()
ax = plt.axes(xlim=(1e3, 1e9))
plot, = ax.semilogx (freqs, data)
plt.xlabel ("Frequency (Hz)")
plt.ylabel ("Amplitude (dB, uncalibrated)")
plt.title ("Voltage Insertion Gain, uncalibrated")
plt.grid (True)

plt.draw ()
plt.waitforbuttonpress (-1)

print ("Collecting data... ")
freqs = np.logspace(3, 8.1761, 60) # 1 kHz to 150 MHz
data = []
for i in freqs:
    s.write (("T:FREQ 1, %f\r\n" % i).encode ('ascii'))
    getline (s)
    s.write (b"T:SAM 5000\r\n")
    level = float (getline (s))
    db = level / (4095 * 24e-3 / 3.3)
    print ("%.2f Hz\t%.2f dB" % (i, db))
    data.append (db)

data = [i-data[0] for i in data]

ax.semilogx (freqs, data)
plt.xlabel ("Frequency (Hz)")
plt.ylabel ("Amplitude (dB, uncalibrated)")
plt.title ("Voltage Insertion Gain, uncalibrated")
plt.grid (True)

plt.draw ()
plt.waitforbuttonpress (-1)
plt.savefig('out.png')
