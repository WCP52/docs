#!/usr/bin/python
import serial
import time
import sys
from serial_comm import getline
import serial_comm as defs

# The first few samples come out wrong. Repeat them
N_REPEAT = 6

def get_freq_response(s, freqs, statusbar=None):
    print ("Collecting data... ")
    data = []

    freqs = list(freqs[:N_REPEAT]) + list(freqs)

    for n, i in enumerate(freqs):
        if statusbar is not None:
            percentage = 100.0 * ((1+n) / len(freqs))
            statusbar.set("Gain: {pct:.0f}%% (at {freq:.2f} Hz)".format(pct=percentage, freq=i))
        nSamples = max(((1/i)*50)//1000000, 2048)
        s.write (("T:FREQ %d, %f\r\n" % (defs.CH_MAIN, i)).encode ('ascii'))
        getline (s)
        s.write(b"LOW:CLR GPIO_ATTEN\r\n")
        time.sleep(.005)
        s.write (("T:SAM %d\r\n" % nSamples).encode ('ascii'))
        level = float (getline (s))
        
        #if level >= 2900, attenuate the input signal
        if level >= 3500:
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

    if statusbar is not None:
        statusbar.set ("")

    # Remove repeated measurements
    data = data[N_REPEAT:]
    #data = [i-data[0] for i in data]
    return data


def get_phase_response(s, freqs, statusbar=None):
    print ("Collecting phase data...")
    N_POINTS_PER_RANGE = 8
    PRECISION = 5.
    data = []
    freqs = list(freqs[:N_REPEAT]) + list(freqs)
    for n, i in enumerate(freqs):
        if statusbar is not None:
            percentage = 100.0 * ((1+n) / len(freqs))
            statusbar.set("Phase: {pct:.0f}%% (at {freq:.2f} Hz)".format(pct=percentage, freq=i))

        # Set frequency. Then, search phases for a null
        s.write (("T:FREQ %d, %f\r\n" % (defs.CH_PHASE, i)).encode ('ascii'))
        getline (s)
        s.write (("T:FREQ %d, %f\r\n" % (defs.CH_MAIN, i)).encode ('ascii'))
        getline (s)
        s.write (("T:AMP %d, 1.0\r\n" % (defs.CH_PHASE)).encode ('ascii'))
        getline (s)
        s.write(b"LOW:SET GPIO_ATTEN\r\n")
        s.write (("T:AMP %d, 0.178\r\n" % (defs.CH_MAIN)).encode ('ascii'))
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
                nSamples = max(((1/i)*50)//1000000, 2048)
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

    if statusbar is not None:
        statusbar.set ("")

    data = data[N_REPEAT:]
    return data

