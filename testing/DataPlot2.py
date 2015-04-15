#!usr/bin/env/python2.7

try:
	from Tkinter import *
except ImportError:
	from tkinter import * 
import tkMessageBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

root =  Tk()
root.geometry("365x245")
## ####test values THIS MUST BE REPLACED#######
random_list = []
 
###############################################

 
#####################################################

## outputting arbitrary values read in list in text widget will need to wrap  on Chris function 

def Calibrate():
	print v		
def GraphPlot():
	global random_list
	plt.plot(random_list)
	plt.axis([0,40,0,40])
	plt.savefig('out.png')	
	plt.show()
	
#def ErrorBox():
#	tkMessageBox.showerror("Error", "Invalid Input.")
	
#ErrorBox()
 

###############################################################################################

Calibrating = Button(root, text= "Calibrate ", fg="Black", command = Calibrate).grid(row = 0, column = 0)
 
  
displayGraph = Button(root, text="Generate Plot", fg="Black", command = GraphPlot ).grid(row = 0, column = 1)

CheckVar1 = IntVar()
C1 = Checkbutton(root, text = "Linear", variable = CheckVar1, onvalue = 1, offvalue = 0, height=5,  width = 20).grid(row = 1, column = 0)

CheckVar2 = IntVar()
C2 = Checkbutton(root, text = "Phase", variable = CheckVar2,  onvalue = 1, offvalue = 0, height=5,  width = 20).grid(row = 1, column = 1)

LabMin = Label(root, text="Max").grid(column = 1 , row = 6)
v = DoubleVar()

UserSetMin = Entry(root, bd = 1, textvariable = v ).grid(column = 0 , row = 5)

LabMax = Label(root, text = "Min").grid(column = 0, row = 6)

UserSetMax = Entry(root, bd = 1).grid(column = 1, row = 5)

root.mainloop()
