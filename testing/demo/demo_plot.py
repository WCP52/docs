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

plt.subplot(2, 1, 1)
#ax = plt.axes(xlim=(1e3, 1e9))
plot, = plt.semilogx (freqs, data)
plt.xlabel ("Frequency (Hz)")
plt.ylabel ("Amplitude (dB, uncalibrated)")
plt.title ("Voltage Insertion Gain, uncalibrated")
plt.grid (True)

#plt.draw ()
#plt.waitforbuttonpress (-1)
#
print ("Collecting phase data...")
N_POINTS_PER_RANGE = 4
PRECISION = 10.
freqs = np.logspace(3, 8.1761, 20) # 1 kHz to 150 MHz
data = []
for i in freqs:
    # Set frequency. Then, search phases for a null
    s.write (("T:FREQ 1, %f\r\n" % i).encode ('ascii'))
    getline (s)
    s.write (("T:FREQ 0, %f\r\n" % i).encode ('ascii'))
    getline (s)
    s.write (b"T:AMP 1, 0.5\r\n")
    getline (s)
    s.write (b"T:AMP 0, 0.1\r\n")
    getline (s)

    phase_bound_left = 0
    phase_bound_right = 360
    while phase_bound_right - phase_bound_left > PRECISION:
        width = phase_bound_right - phase_bound_left
        pitch = width / N_POINTS_PER_RANGE
        phases = [(i * pitch) + phase_bound_left for i in range (N_POINTS_PER_RANGE)]
        lowest_phase = None
        lowest_amp = float("inf")
        lowest_i = None
        for phase_i, phase in enumerate(phases):
            phase = phase % 360.
            s.write (("T:PHASE 0, %f\r\n" % phase).encode ('ascii'))
            getline (s)
            s.write (b"T:SAM 5000\r\n")
            level = float (getline (s))
            if level < lowest_amp:
                lowest_amp = level
                lowest_phase = phase
                lowest_i = phase_i
            print (".", end='')
            sys.stdout.flush ()
        if lowest_i == 0:
            # Slide the range left
            width = phase_bound_right - phase_bound_left
            phase_bound_left -= width / 2
            phase_bound_right -= width / 2
        elif lowest_i == len(phases) - 1:
            # Slide the range right
            width = phase_bound_right - phase_bound_left
            phase_bound_left += width / 2
            phase_bound_right += width / 2
        else:
            # Narrow the range
            phase_bound_left = phases[lowest_i - 1]
            phase_bound_right = phases[lowest_i + 1]

    phases = list (range (0, 360, 40))
    lowest_phase -= 180.

    # Smooth phase discontinuities
    if len(data):
        last_phase = data[-1]
        offset_phases = [phase + (360. * i) for i in range(-3,4)]
        phase_errors = [abs(i - last_phase) for i in offset_phases]

        best_phase, best_error = min (zip (offset_phases, phase_errors), key=lambda x: x[1])
        phase = best_phase


    print ("%.2f Hz\t%f deg" % (i, phase))
    data.append (phase)

plt.subplot(2, 1, 2)
#ax = plt.axes(xlim=(1e3, 1e9))
plot, = plt.semilogx (freqs, data)
plt.xlabel ("Frequency (Hz)")
plt.ylabel ("Phase (deg, uncalibrated)")
plt.title ("Phase Shift, uncalibrated")
plt.grid (True)

plt.savefig('out.png')
plt.show ()
#plt.waitforbuttonpress (-1)


s.write (b"T:AMP 1, 0\r\n")
getline (s)
s.write (b"T:AMP 0, 0\r\n")
getline (s)
