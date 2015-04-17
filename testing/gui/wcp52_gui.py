#!/usr/bin/env python

try:
	from Tkinter import *
except ImportError:
	from tkinter import *
import matplotlib.pyplot as plt
from bode import Bode

root =  Tk()
root.geometry("365x245")
 
bode_plot = Bode()

startGraph = Button(root, text= "Calibrate ", fg="Black", command = bode_plot.calibrate).grid(row = 0, column = 0)
  
displayGraph = Button(root, text="Generate Plot", fg="Black", command = bode_plot.display_plot ).grid(row = 0, column = 1)

C1 = Checkbutton(root, text = "Linear", variable = bode_plot.do_linear, onvalue = True, offvalue = False, height=5,  width = 20).grid(row = 1, column = 0)

C2 = Checkbutton(root, text = "Phase", variable = bode_plot.do_phase,  onvalue = True, offvalue = False, height=5,  width = 20).grid(row = 1, column = 1)


LabMin = Label(root, text="Min").grid(column = 1 , row = 6)

UserSetMin = Entry(root, bd = 1, textvariable = bode_plot.lower_bound).grid(column = 0 , row = 5)

LabMax = Label(root, text = "Max").grid(column = 0, row = 6)

UserSetMax = Entry(root, bd = 1, textvariable = bode_plot.upper_bound).grid(column = 1, row = 5)


root.mainloop()
