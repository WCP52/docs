#!usr/bin/python

try:
	from Tkinter import *
except ImportError:
	from tkinter import *
from PIL import Image
from PIL import ImageTk 
##import tkMessageBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

root =  Tk()
Left =  Frame(root)
Right = Frame(root)
#frame =  PanedWindow(orient=HORIZONTAL)
Left.pack(side = LEFT)
Right.pack(side= RIGHT,fill =BOTH, expand = 1) 
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
	text = Text(Left)
	for x in random_list2:
		text.insert(END, x + '\n')
	
	text.pack(in_ = Left, side = BOTTOM)
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
	plt.savefig('out.png')	
	ImagePlot = Image.open("out.png")
	Plotphoto = ImageTk.PhotoImage(ImagePlot)
	PlotLabel = Label(root,Plotphoto)## Problem line
	PlotLabel.image = Plotphoto
	PlotLabel.pack(in_ = Right)
	plt.show()
	
RandomNumGen()
ConvertListToString()
 

###############################################################################################

startGraph = Button(Left, text= "Calibrate ", fg="Black", command = textInsert)
startGraph.pack( in_ = Left, side = TOP )
  
displayGraph = Button(Left, text="Generate Plot", fg="Black", command = GraphPlot )
displayGraph.pack( in_ = Left, side = TOP )

CheckVar1 = IntVar()
C1 = Checkbutton(Left, text = "Linear", variable = CheckVar1, onvalue = 1, offvalue = 0, height=5,  width = 20)
C1.pack(in_ = Left,side = TOP)

CheckVar2 = IntVar()
C2 = Checkbutton(Left, text = "Phase", variable = CheckVar2,  onvalue = 1, offvalue = 0, height=5,  width = 20)
C2.pack(in_ =Left, side = TOP)


LabMin = Label(Left, text="Min")
LabMin.pack( side =BOTTOM )

UserSetMin = Entry(Left, bd = 1 )
UserSetMin.pack(side = BOTTOM)

LabMax = Label(Left, text = "Max")
LabMax.pack( side =  BOTTOM)

UserSetMax = Entry(Left, bd = 1)
UserSetMax.pack(side = BOTTOM)



root.mainloop()
