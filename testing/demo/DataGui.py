#!usr/bin/python

from Tkinter import *
import tkMessageBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
##style.use("ggplot")
##f = Figure(figsize=(5,5), dpi=100)
##a = f.add_subplot(111)

top =  Tk()
frame =  Frame(top)
frame.pack()

phases = [12,32,42,23, 42,12,34]
freq = [2,3,4,5,6,7,8]

bottomframe = Frame(top)
bottomframe.pack( side = BOTTOM)

redbutton = Button(frame, text="INCR", fg="Black")
redbutton.pack( side = LEFT )

brownbutton = Button(frame, text="FREQ", fg="Black")
brownbutton.pack( side = LEFT )

bluebutton = Button(frame, text="PHASE", fg="Black")
bluebutton.pack( side = LEFT )

blackbutton = Button(frame, text="GRAPH", fg="Black")
blackbutton.pack( side = LEFT )

text = Text(top)
text.insert([phases],'dfdfdf')
text.pack(side = BOTTOM)

plot = plt.plot (phases,frequency)
 
top.mainloop()
