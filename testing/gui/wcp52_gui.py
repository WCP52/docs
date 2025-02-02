#!/usr/bin/env python

try:
    import tkinter as tk
except:
    import Tkinter as tk
import pygubu
import matplotlib
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from bode import Bode
import threading

class GUI:
    def __init__(self, master):

        self.builder = builder = pygubu.Builder()
        builder.add_from_file("GUI.ui")
        master.title("USB Gain/Phase Analyzer")
        #master.rowconfigure(0, weight=1)
        #master.columnconfigure(0, weight=1)
        self.top = builder.get_object("top", master)
        
        # Status bar
        self.statusbar = StatusBar(self.top)
        self.statusbar.grid(column=0,columnspan=5,row=15)
        self.statusbar.set("...status...")

        #Set up entry boxes
        self.min_var = tk.DoubleVar()
        self.min_var.set(1e3)
        self.max_var = tk.DoubleVar()
        self.max_var.set(150e6)
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

        self.bode = Bode()
        
    def on_plot(self):
        self.freq_fig.clear()
        self.phase_fig.clear()
        phase = self.builder.get_variable('do_phase').get()
        linear = self.builder.get_variable('do_linear').get()


        #If we have not calibrated, then we need to make sure that these
        #Bode attributes have been set
        if not self.calibrate:
            lower_bound = self.min_var.get() 
            upper_bound = self.max_var.get()
            # need error here
            #while lower_bound != upper_bound:
            if lower_bound >= upper_bound:
                error = tk.messagebox.showerror("error","These values are not valid.\n Try again min must be lower than max" )
            #        break
            self.bode.set_lower_bound(lower_bound)
            self.bode.set_upper_bound(upper_bound)
            self.bode.set_do_phase(phase)
            self.bode.generate_freqs()

        def callback():
            #Get frequency response data from bode.
            freq_response = self.bode.get_freq_response_data()
            if self.calibrate:
                freq_plt = self.freq_fig.add_subplot(111, xlabel="Frequency", ylabel="Gain, calibrated")
                freq_calibrate_data = self.bode.get_freq_calibration_data()
                assert len(freq_calibrate_data) == len(freq_response), (len(freq_calibrate_data), len(freq_response))
                for i in range(len(freq_response)):
                    freq_response[i] = freq_response[i] - freq_calibrate_data[i]
            else:
                freq_plt = self.freq_fig.add_subplot(111, xlabel="Frequency", ylabel="Gain, uncalibrated")
            
            #Generate frequency response plot
            freqs_f = self.bode.get_freqs_f()
            if not linear:
                freq_plt.semilogx(freqs_f, freq_response)
            else:
                freq_plt.plot(freqs_f, freq_response)
            freq_plt.grid(True)
            self.freq_canvas.show()
            self.freq_canvas.get_tk_widget().place(relx=.26, rely=0.01,relheight=0.49,relwidth=0.7)

            #If we want phase, we go through the process again
            if phase:
                phase_response = self.bode.get_phase_response_data()
                if self.calibrate:
                    phase_plt = self.phase_fig.add_subplot(111, xlabel="Frequency", ylabel="Phase, calibrated")
                    phase_calibrate_data = self.bode.get_phase_calibration_data()
                    for i in range(len(phase_response)):
                        phase_response[i] = phase_response[i] - phase_calibrate_data[i]
                else:
                    phase_plt = self.phase_fig.add_subplot(111, xlabel="Frequency", ylabel="Phase, uncalibrated")

                freqs_p = self.bode.get_freqs_p()

                if not linear:
                    phase_plt.semilogx(freqs_p, phase_response)
                else:
                    phase_plt.plot(freqs_p, phase_response)

                phase_plt.grid(True)
                self.phase_canvas.show()
                self.phase_canvas.get_tk_widget().place(relx=.26,rely=0.505,relheight=0.49,relwidth=0.7)

        #Have bode generate data
        self.bode.run_threaded(self.statusbar, callback)

        
    def on_calibrate(self):
        #set lower and upper bounds for bode
        lower_bound = self.min_var.get()
        upper_bound = self.max_var.get()
        self.bode.set_lower_bound(lower_bound)
        self.bode.set_upper_bound(upper_bound)
        #need error box here
        #while lower_bound != upper_bound:
        if lower_bound >= upper_bound:
            error = tk.messagebox.showerror("error","These values are not valid.\n Try again min must be lower than max")
        #        break
        #tell bode whether or not it will do a phase plot
        phase = self.builder.get_variable('do_phase').get()
        self.bode.set_do_phase(phase)

        #generate the frequencies to sample across
        self.bode.generate_freqs()

        #have bode perform calibration
        def callback():
            self.calibrate = True
        self.bode.calibrate_threaded(self.statusbar, callback)

class StatusBar(tk.Frame):
   def __init__(self, master):
      tk.Frame.__init__(self, master)
      self.label = tk.Label(self, bd = 1, relief = tk.SUNKEN, anchor = "w")
      self.label.pack(fill=tk.X)
   def set(self, format0, *args):
      self.label.config(text = format0 % args)
      self.label.update_idletasks()
   def clear(self):
      self.label.config(text="")
      self.label.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
