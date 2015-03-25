#!/usr/bin/python

try:
	from Tkinter import *
except ImportError:
	from tkinter import *
#from PIL import Image 
##import tkMessageBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
 
top =  Tk()
frame =  PanedWindow(orient=HORIZONTAL)
frame.pack(fill =BOTH, expand = 1) 
## ####test values THIS MUST BE REPLACED#######
##phases = ['12','32','42','23', '42','12','34']
##phases2 = [12,32,42,23,42,12,34]
##freq = [2,3,4,5,6,7,8]
random_list = []
 
###############################################

 
#####################################################

## outputting arbitrary values read in list in text widget will need to wrap  on Chris function 

def ConvertListToString():
	global random_list2
	random_list2 = ' '.join(str(x) for x in random_list)
	print(random_list2)
def textInsert():
	ConvertListToString()
	text = Text(top)
	for x in random_list2:
		text.insert(END, x + '\n')
	
	text.pack(side = LEFT)
##	frame.add(text)
##	plt.plot (phases)
##	plt.axis([0,8,0,40])
##	plt.show()
##      PlotImage = PhotoImage(file = "plotPic.gif")
##	Pic = Label(frame, PlotImage)
##	Pic.pack()
##	frame.add(Pic) 
def RandomNumGen():
	for i in range(10):
		random_list.append(random.randrange(1,101,1))
	print(random_list)
 
##def stopButton():
	
def GraphPlot():
	global random_list
	plt.plot(random_list)
	plt.axis([0,40,0,40])	
	plt.show()
RandomNumGen()
ConvertListToString()
 

  

	
###############################################################################################

startGraph = Button(frame, text= "Start Plot ", fg="Black", command = textInsert)

startGraph.pack( side = LEFT )
##stopGraph = Button(frame, text="Stop Graph", fg= "Black") 
##stopGraph.pack( side = LEFT )
displayGraph = Button(frame, text="Display Graph", fg="Black", command = GraphPlot )
displayGraph.pack( side = LEFT )
CheckVar1 = IntVar()
CheckVar2 = IntVar()
C1 = Checkbutton(top, text = "Freq", variable = CheckVar1, onvalue = 1, offvalue = 0, height=5,  width = 20)
C2 = Checkbutton(top, text = "Phase", variable = CheckVar2,  onvalue = 1, offvalue = 0, height=5,  width = 20)
C1.pack(side = LEFT)
C2.pack(side = LEFT)

top.mainloop()
