#!/usr/bin/python
import serial
import time
import sys
from demo_plot_defs import getline
import demo_plot_defs as defs

def get_freq_response(s, freqs):
    print ("Collecting data... ")
    data = []
    for i in freqs:
        nSamples = max(((1/i)*25)//1000000, 1024)
        s.write (("T:FREQ %d, %f\r\n" % (defs.CH_MAIN, i)).encode ('ascii'))
        getline (s)
        s.write(b"LOW:CLR GPIO_ATTEN\r\n")
        time.sleep(.005)
        s.write (("T:SAM %d\r\n" % nSamples).encode ('ascii'))
        level = float (getline (s))
        
        #if level >= 2900, attenuate the input signal
        if level >= 2900:
            print("this is running...")
            s.write(b"LOW:SET GPIO_ATTEN\r\n")
            time.sleep(.005)
            s.write (("T:SAM %d\r\n" % nSamples).encode ('ascii'))
            level = float (getline (s))
            db = level / (4095 * 24e-3 / 3.3) + 15
        else: 
            db = level / (4095 * 24e-3 / 3.3)

        print ("%.2f Hz\t%.2f dB" % (i, db))
        data.append (db)

    data = [i-data[0] for i in data]
    return data


def get_phase_response(s, freqs):
    print ("Collecting phase data...")
    N_POINTS_PER_RANGE = 10
    PRECISION = 1.
    data = []
    for i in freqs:
        # Set frequency. Then, search phases for a null
        s.write (("T:FREQ %d, %f\r\n" % (defs.CH_PHASE, i)).encode ('ascii'))
        getline (s)
        s.write (("T:FREQ %d, %f\r\n" % (defs.CH_MAIN, i)).encode ('ascii'))
        getline (s)
        s.write (("T:AMP %d, 0.5\r\n" % (defs.CH_PHASE)).encode ('ascii'))
        getline (s)
        s.write (("T:AMP %d, 0.1\r\n" % (defs.CH_MAIN)).encode ('ascii'))
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
                nSamples = max(((1/i)*25)//1000000, 1024)
                phase = phase % 360.
                s.write (("T:PHASE %d, %f\r\n" % (defs.CH_PHASE, phase)).encode ('ascii'))
                getline (s)
                s.write (("T:SAM %d\r\n" % nSamples).encode ('ascii'))
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
        phase = lowest_phase

        # Smooth phase discontinuities
        if len(data):
            last_phase = data[-1]
            offset_phases = [phase + (360. * i) for i in range(-3,4)]
            phase_errors = [abs(i - last_phase) for i in offset_phases]

            best_phase, best_error = min (zip (offset_phases, phase_errors), key=lambda x: x[1])
            phase = best_phase


        print ("%.2f Hz\t%f deg" % (i, phase))
        data.append (phase)
    return data

