#!/usr/bin/python
import serial
import time

def getline (s):
    return s.readline ().decode ('ascii').strip ()

def printline (s, indent=2):
    """Print a line from serial, indented."""
    line = getline (s)
    print ((" " * indent) + line)
    return line

def connect_gpa():
    print ("Connecting to GPA...")
    return serial.Serial ("/dev/ttyACM0", 115200, timeout=1)

def mc_init(s):
    print ("Initializing microcontroller...")
    s.write (b"*RST\r\n")
    s.read (100)
    time.sleep (0.5)
    s.flushInput ()
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
    s.write (b"T:FREQ 0, 0\r\n")
    printline (s)
    s.write (b"T:AMP 0, 0\r\n")
    printline (s)
    s.write (b"T:CH 1\r\n")
    s.write (b"*OPC?\r\n")
    getline (s)
    print ("  OK")

