#!/usr/bin/python2.7

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import sys
import time
from demo_plot_defs import *
from other_funcs import get_freq_response, get_phase_response


if (sys.argv[1] == "help"):
    print ("usage: demo_plot.py MIN MAX options...")
    print ("MIN MAX define the range of frequencies to test")
    print ("Possible options: linear, phase, calibrate.")
    print ("linear will produce a linear plot instead of a logarithmic one")
    print ("phase will produce a phase response in addition to the frequency response plot")
    print ("calibrate is recommended and allows you to run an extra test with just a copper wire to better calibrate the final output.")
    print ("")
    sys.exit (1)
elif len(sys.argv) < 3:
    print ("usage: demo_plot.py MIN MAX options...")
    sys.exit (1)
try:
    float (sys.argv[1])
    float (sys.argv[2])
except ValueError:
    print ("usage: demo_plot.py MIN MAX options...")
    print ("MIN and MAX must be floating point!")
    sys.exit (1)

#Initialize 
s = connect_gpa()
mc_init(s)
synth_init(s)
frontend_init(s)


lower_bound = float (sys.argv[1])
upper_bound = float (sys.argv[2])



freqs_f = np.logspace(np.log10(lower_bound), np.log10(upper_bound), 60) # 1 kHz to 150 MHz
freqs_p = np.logspace(np.log10(lower_bound), np.log10(upper_bound), 30) # 1 kHz to 150 MHz
data_f = []
data_p = []
data_calibrate_f = []
data_calibrate_p = []


if "calibrate" in sys.argv:
    input ("Please double check that the wire is connected and press Enter...")
    data_calibrate_f = get_freq_response(s, lower_bound, upper_bound, freqs_f)
    if "phase" in sys.argv:
        data_calibrate_p = get_phase_response(s, lower_bound, upper_bound, freqs_p)

input ("Now connect your filter for testing and press Enter ...")
data_f = get_freq_response(s, lower_bound, upper_bound, freqs_f)
if "calibrate" in sys.argv:
    for i in range(len(data_f)):
        data_f[i] = data_f[i] - data_calibrate_f[i]
plt.subplot(2, 1, 1)
#ax = plt.axes(xlim=(1e3, 1e9))
if 'linear' in sys.argv:
    plot, = plt.plot (freqs_f, data_f)
else:
    plot, = plt.semilogx (freqs_f, data_f)
if "phase" not in sys.argv:
    plt.xlabel ("Frequency (Hz)")
plt.ylabel ("Amplitude (dB, calibrated)")
plt.title ("Voltage Insertion Gain, calibrated")
plt.grid (True)

if "phase" in sys.argv:
    data_p = get_phase_response(s, lower_bound, upper_bound, freqs_p)
    if "calibrate" in sys.argv:
        for i in range(len(data_p)):
            data_p[i] = data_p[i] - data_calibrate_p[i]
    plt.subplot(2, 1, 2)
    #ax = plt.axes(xlim=(1e3, 1e9))
    if 'linear' in sys.argv:
        plot, = plt.plot (freqs_p, data_p)
    else:
        plot, = plt.semilogx (freqs_p, data_p)
    plt.xlabel ("Frequency (Hz)")
    plt.ylabel ("Phase (deg, calibrated)")
    plt.title ("Phase Shift, calibrated")
    plt.grid (True)

plt.savefig('out.png')
plt.show ()

