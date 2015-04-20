#!/usr/bin/end python

from serial_comm import *
from response import *

class Bode:
    def __init__(self):
        self.s = connect_gpa()
        mc_init(self.s)
        synth_init(self.s)
        frontend_init(self.s)
        self.freq_calibration = []
        self.phase_calibration = []
        self.freq_response = []
        self.phase_response = []
        self.freqs_f = []
        self.freqs_p = []
        self.upper_bound = 0.0
        self.lower_bound = 0.0
        self.do_phase = False

    #set the upper bound of sampling frequencies
    def set_upper_bound(self, upper_bound):
        self.upper_bound = upper_bound

    #sets lower bound of sampling frequencies
    def set_lower_bound(self, lower_bound):
        self.lower_bound = lower_bound

    def set_do_phase(self, do_phase):
        self.do_phase = do_phase

    def get_freq_calibration_data(self):
        return self.freq_calibration
    
    def get_phase_calibration_data(self):
        return self.phase_calibration

    def get_freq_response_data(self):
        return self.freq_response
    
    def get_phase_response_data(self):
        return self.phase_response

    #generate lists of all sampling frequencies
    def generate_freqs(self):
        self.freqs_f = np.logspace(np.log10(self.lower_bound), np.log10(self.upper_bound), 60) # 1 kHz to 150 MHz
        if self.do_phase:
            self.freqs_p = np.logspace(np.log10(self.lower_bound), np.log10(self.upper_bound), 30) # 1 kHz to 150 MHz

    def get_freqs_f(self):
        return self.freqs.f

    def get_freqs_p(self):
        return self.freqs.p

    def calibrate(self):
        self.freq_calibration = get_freq_response(self.s, self.freqs_f)
        if self.do_phase:
            self.phase_calibration = get_phase_response(self.s, self.freqs_p)

    def run(self):
        self.freq_response = get_freq_response(self.s, self.freqs_f)
        if self.do_phase:
            self.phase_response = get_phase_response(self.s, self.freqs_p)


    
    
