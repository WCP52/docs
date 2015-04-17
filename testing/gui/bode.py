#!/usr/bin/end python

import time
import sys
import matplotlib.pyplot as plt
import numpy as np

from serial_comm import *
from response import *

class Bode:
    def __init__(self):
        """
        self.s = connect_gpa()
        mc_init(self.s)
        synth_init(self.s)
        frontend_init(self.s)
        """
        self.freq_calibration = []
        self.phase_calibration = []
        self.freq_response = []
        self.phase_response = []
        self.freqs_f = []
        self.freqs_p = []
        self.upper_bound = 0.0
        self.lower_bound = 0.0
        self.do_phase = False
        self.do_linear = False 
    
    def calibrate(self):
 
        self.freqs_f = np.logspace(np.log10(self.lower_bound), np.log10(self.upper_bound), 60) # 1 kHz to 150 MHz
        self.freq_calibration = get_freq_response(self.s, self.freqs_f)
        if self.do_phase:
            self.freqs_p = np.logspace(np.log10(lower_bound), np.log10(upper_bound), 30) # 1 kHz to 150 MHz
            self.phase_calibration = get_phase_response(self.s, self.phase)

    def display_plot(self):
        self.freqs_f = np.logspace(np.log10(self.lower_bound), np.log10(self.upper_bound), 60) # 1 kHz to 150 MHz
        self.freq_response = get_freq_response(self.s, self.freqs_f)
        if self.do_phase:
            self.freqs_p = np.logspace(np.log10(lower_bound), np.log10(upper_bound), 30) # 1 kHz to 150 MHz
            self.phase_response = get_phase_response(self.s, self.freqs_p)
        if self.freq_calibration:
            for i in range(len(self.freq_response)):
                self.freq_response = self.freq_response[i] - self.freq_calibration[i]
        plt.subplot(2,1,1)
        if do_linear:
            plot = plt.plot(self.freqs_f, self.freq_response)
        else:
            plot = plt.semilogx(self.freqs.f, self.freq_response)
        if not do_phase:
            plt.xlabel ("Frequency (Hz)")
        plt.ylabel ("Amplitude (dB, calibrated)")
        plt.title ("Voltage Insertion Gain, calibrated")
        plt.grid (True)
        if do_phase:
            plt.subplot(2,1,2)
            if do_linear:
                plot, = plt.plot (self.freqs_p, self.data_p)
            else:
                plot, = plt.semilogx (freqs_p, data_p)
            plt.xlabel ("Frequency (Hz)")
            plt.ylabel ("Phase (deg, calibrated)")
            plt.title("Phase Shift, calibrated")
            plt.grid(True)
        plt.show()
