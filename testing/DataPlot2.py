#!/usr/bin/python2.7

try:
	from Tkinter import *
except ImportError:
<<<<<<< HEAD
	from tkinter import * 
#import tkMessageBox
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
=======
	from tkinter import *
import tkMessageBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
>>>>>>> f901a5a44410eea8a7a6a4de2798daded396f252
import random

root =  Tk()
root.geometry("365x245")
random_list = []
 
###############################################

 
#####################################################
<<<<<<< HEAD

## outputting arbitrary values read in list in text widget will need to wrap  on Chris function 

def Calibrate():
	print("Min:" + str(v.get())+" "+"Max:"+ " " + str(v2.get()))		
=======
>>>>>>> f901a5a44410eea8a7a6a4de2798daded396f252
def GraphPlot():
	plt.plot(random_list)
	plt.axis([0,40,0,40])
	plt.savefig('out.png')	
	plt.show()

def calibrate():
    print "min: " + str(min_value.get()), 
    print "max: " + str(max_value.get())

###############################################################################################

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
<<<<<<< HEAD
v2 = DoubleVar()
UserSetMax = Entry(root, bd = 1, textvariable = v2).grid(column = 1, row = 5)
=======
max_value = DoubleVar()
UserSetMax = Entry(root, bd = 1, textvariable = max_value).grid(column = 1, row = 5)

>>>>>>> f901a5a44410eea8a7a6a4de2798daded396f252

root.mainloop()
