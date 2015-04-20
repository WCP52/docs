#!/usr/bin/env python

try:
    import tkinter as tk
except:
    import Tkinter as tk
import pygubu
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GUI:
    def __init__(self, master):

        self.builder = builder = pygubu.Builder()
        builder.add_from_file("GUI.ui")
        master.title("USB Gain/Phase Analyzer")
        #master.rowconfigure(0, weight=1)
        #master.columnconfigure(0, weight=1)
        self.top = builder.get_object("top", master)
        
        #Set up entry boxes
        self.min_var = tk.DoubleVar()
        self.max_var = tk.DoubleVar()
        self.min_entry = tk.Entry(self.top, name="entry_min",textvariable=self.min_var, width=10)
        self.min_entry.grid(column=1,row=1)
        self.max_entry = tk.Entry(self.top, name="entry_max", textvariable=self.max_var,width=10)
        self.max_entry.grid(column=1,row=2)

        #set up canvas to hold plots
        self.freq_fig = Figure()
        self.phase_fig = Figure()
        self.freq_canvas = FigureCanvasTkAgg(self.freq_fig, master)
        self.phase_canvas = FigureCanvasTkAgg(self.phase_fig, master)

        #connect callbacks
        builder.connect_callbacks(self)
        self.calibrate = False
        
    def on_plot(self):
        self.freq_fig.clear()
        self.phase_fig.clear()
        phase = self.builder.get_variable('do_phase').get()
        linear = self.builder.get_variable('do_linear').get()
        min_val = self.min_var.get() 
        max_val = self.max_var.get()
        #phase = self.cb_phase.get() 
        
        x = [x for x in range(int(min_val),int(max_val),1)]
        y = [y**3 for y in x]
        
        if self.calibrate:
            freq_plt = self.freq_fig.add_subplot(111, xlabel="x", ylabel="y=x**3, calibrated")
        else:
            freq_plt = self.freq_fig.add_subplot(111, xlabel="x", ylabel="y=x**3, uncalibrated")
        
        if not linear:
            freq_plt.semilogx(x,y)
        else:
            freq_plt.plot(x,y)

        self.freq_canvas.show()
        self.freq_canvas.get_tk_widget().place(relx=.26, rely=0.01,relheight=0.49,relwidth=0.7)

        if phase:
            y = [y**2 for y in x]
            
            if self.calibrate:
                phase_plt = self.phase_fig.add_subplot(111, xlabel="x", ylabel="y=x**2, calibrated")
            else:
                phase_plt = self.phase_fig.add_subplot(111, xlabel="x", ylabel="y=x**2, uncalibrated")
            if not linear:
                phase_plt.semilogx(x,y)
            else:
                phase_plt.plot(x,y)

            self.phase_canvas.show()
            self.phase_canvas.get_tk_widget().place(relx=.26,rely=0.505,relheight=0.49,relwidth=0.7)
        
    def on_calibrate(self):
        self.calibrate = True

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
