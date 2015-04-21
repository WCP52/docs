#!/usr/bin/env python


"""
This file contains the functions necessary to establish and use
a serial connection to the Gain/Phase Analyzer

In order to set up a connection to the gain/phase analyzer properly,
you must first call connect_gpa().  It returns a serial object which
is then used to initialize board peripherals.  It can be used like this:
    s = connect_gpa()
    mc_init(s)
    synth_init(s)
    frontend_init(s)

"""

import os
import serial
import time

USB_ID = "1209:4757"

def read(fn):
    with open (fn) as f:
        return f.read().strip()

def usb_id(path):
    if not os.path.isfile (path + "/idProduct"):
        return None
    if not os.path.isfile (path + "/idVendor"):
        return None
    product = read(path + "/idProduct")
    vendor = read(path + "/idVendor")
    return vendor.lower() + ":" + product.lower()

def get_tty(path):
    for subdir in os.listdir(path):
        if not os.path.isdir(path + "/" + subdir):
            continue
        if os.path.isdir(path + "/" + subdir + "/tty"):
            this_subdir = subdir
            break
    return "/dev/" + os.listdir(os.path.join(path, subdir, "tty"))[0]


def find_device():
    DEVS = "/sys/bus/usb/devices"
    for dev_dir in os.listdir(DEVS):
        path = DEVS + "/" + dev_dir
        if usb_id(path) == USB_ID:
            return DEVS + "/" + dev_dir


# Read the latest data that was sent across the serial interface.
def getline (s):
    return s.readline ().decode ('ascii').strip ()

# Print the data read from the serial interface
def printline (s, indent=2):
    """Print a line from serial, indented."""
    line = getline (s)
    print ((" " * indent) + line)
    return line

# Sets up a serial connection to the gain phase analyzer.  This function
# must be called before the functions that follow in this file.  It returns
# a serial connection that is used to pass to those functions.
def connect_gpa():
    devnode = find_device()
    if devnode is None:
        raise Exception("No GPA found!")
    tty = get_tty(devnode)
    print ("Connecting to GPA...")
    return serial.Serial (tty, 1, timeout=1)

# Initializes the microcontroller using the serial connection
# which is passed as a parameter
def mc_init(s):
    print ("Testing microcontroller...")
    s.write (b"*IDN?\r\n")
    idnstr = getline (s)
    print ("  identity string = " + idnstr)
    while not idnstr.startswith ("WCP52"):
        print ("  bad response, retrying")
        s.write (b"\r\n\r\n\r\n")
        time.sleep (0.5)
        s.flushOutput ()
        s.flushInput ()
        s.write (b"*IDN?\r\n")
        idnstr = getline (s)
        print ("  identity string = " + idnstr)
    print ("  OK")

# Initializes the synthesizer
def synth_init(s):
    print ("Initializing synthesizer...")
    s.write (b"T:INIF\r\n")
    s.write (b"*OPC?\r\n")
    getline (s)
    time.sleep (0.25)
    s.write (b"T:INCK\r\n")
    s.write (b"*OPC?\r\n")
    getline (s)
    time.sleep (0.25)
    print ("  OK")

#Initializes the front end
def frontend_init(s):
    print ("Initializing frontend... ")
    s.write (b"T:FREQ 0, 0\r\n")
    printline (s)
    s.write (b"T:AMP 0, 0\r\n")
    printline (s)
    s.write (b"T:CH 1\r\n")
    s.write (b"*OPC?\r\n")
    getline (s)
    print ("  OK")

