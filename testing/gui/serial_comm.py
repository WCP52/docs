#!/usr/bin/python
import serial
import time
import os

CH_MAIN = 0
CH_PHASE = 1
CH_IN_1 = 1
CH_IN_2 = 0

USB_ID = "1209:4757"


def getline (s):
    return s.readline ().decode ('ascii').strip ()

def printline (s, indent=2):
    """Print a line from serial, indented."""
    line = getline (s)
    print ((" " * indent) + line)
    return line

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

def connect_gpa():
    devnode = find_device()
    if devnode is None:
        raise Exception("No GPA found!")
    tty = get_tty(devnode)
    print ("Connecting to GPA...")
    return serial.Serial (tty, 1, timeout=1)

def mc_init(s):
    print ("Initializing microcontroller...")
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

def frontend_init(s):
    print ("Initializing frontend... ")
    s.write (("T:FREQ %d, 0\r\n" % (CH_PHASE)).encode('ascii'))
    printline (s)
    s.write (("T:AMP %d, 0\r\n" % (CH_PHASE)).encode('ascii'))
    printline (s)
    s.write (("T:CH %d\r\n" % (CH_IN_1)).encode('ascii'))
    s.write (b"*OPC?\r\n")
    getline (s)
    print ("  OK")

