#!/usr/bin/python2.7

try:
	from Tkinter import *
except ImportError:
	from tkinter import *
import tkMessageBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from response import *
from serial import *

root =  Tk()
root.geometry("365x245")
 
#####################################################
def GraphPlot():
    pass
def calibrate():
    pass
###############################################################################################


#set up serial connection
s = connect_gpa()

#initialize board peripherals
mc_init(s)
synth_init(s)
frontend_init(s)

startGraph = Button(root, text= "Calibrate ", fg="Black", command = calibrate).grid(row = 0, column = 0)
 
  
displayGraph = Button(root, text="Generate Plot", fg="Black", command = GraphPlot ).grid(row = 0, column = 1)

CheckVar1 = IntVar()
C1 = Checkbutton(root, text = "Linear", variable = CheckVar1, onvalue = 1, offvalue = 0, height=5,  width = 20).grid(row = 1, column = 0)

CheckVar2 = IntVar()
C2 = Checkbutton(root, text = "Phase", variable = CheckVar2,  onvalue = 1, offvalue = 0, height=5,  width = 20).grid(row = 1, column = 1)


LabMin = Label(root, text="Max").grid(column = 1 , row = 6)

min_value = DoubleVar()
UserSetMin = Entry(root, bd = 1, textvariable = min_value ).grid(column = 0 , row = 5)

LabMax = Label(root, text = "Min").grid(column = 0, row = 6)
max_value = DoubleVar()
UserSetMax = Entry(root, bd = 1, textvariable = max_value).grid(column = 1, row = 5)


root.mainloop()
