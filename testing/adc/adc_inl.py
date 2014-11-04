#!/usr/bin/env python3

# Rough test of INL in ATSAM4S16C ADC
# Observation: ADC output spans full range from 0 to 4095.

from pylab import *

test_voltages = arange (0.2, 3.3, 0.2)
adc_out = [
    244, 490, 736, 982, 1228, 1474, 1720, 1966, 2212,
    2458, 2704, 2950, 3196, 3442, 3689, 3935, ];

def tee (text, f):
    f.write (text)
    print (text, end='')


# Compute linear fit
fit_slope, fit_inter = polyfit (test_voltages, adc_out, 1)

# Compute ideal outputs under perfect linearity
adc_out_ideal = fit_slope * test_voltages + fit_inter

# Residuals
resid = adc_out - adc_out_ideal

adc_out_fig = figure ()
plot (test_voltages, adc_out)
title ('ATSAM4S16C ADC Output vs Input')
xlabel ('Input (V)')
ylabel ('Output (LSB)')
grid (True)
adc_out_fig.savefig ('adc_out.eps')
adc_out_fig.savefig ('adc_out.png', dpi=72)

adc_resid_fig = figure ()
plot (test_voltages, resid)
title ('ATSAM4S16C ADC Nonlinear Residuals')
xlabel ('Input (V)')
ylabel ('Residual (LSB)')
grid (True)
adc_resid_fig = savefig ('adc_resid.eps')
adc_resid_fig = savefig ('adc_resid.png', dpi=72)
close ()

max_inl = max (abs (resid))

with open ('transcript.txt', 'w') as f:
    tee ("Maximum INL (LSB): %f\n" % max_inl, f)
