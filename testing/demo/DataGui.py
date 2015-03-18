#!usr/bin/python
try:
	from Tkinter import *
except ImportError: 
	from tkinter import *
 
##from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
 
top =  Tk()
frame =  Frame(top)
frame.pack() 
## ####test values THIS MUST BE REPLACED#######
phases = ['12','32','42','23', '42','12','34']
phases2 = [12,32,42,23,42,12,34]
freq = [2,3,4,5,6,7,8]
###############################################

##phase = Label(top, text=phases)
##phase.pack()

## Buttons that still need to be wrapped around a SPI input#######
bottomframe = Frame(top)
bottomframe.pack( side = BOTTOM)
 
#####################################################

## outputting arbitrary values read in list in text widget will need to wrap  on Chris function 

def textInsert():
	text = Text(top)
	for x in phases:
		text.insert(END, x + '\n')
##text.insert([phases],'dfdfdf')
		text.pack(side = BOTTOM)
###############################################################################################
	plt.plot (phases)
	plt.axis([0,8,0,40])
	plt.show()
startbutton = Button(frame, text= "Start", fg= "Black", command = textInsert)
startbutton.pack(side = TOP)
top.mainloop()
