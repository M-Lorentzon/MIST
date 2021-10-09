import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from Util.csv_string_human_readable import *

class Text_Plotter:

    def __init__(self, master_frame):
        self.master_frame = master_frame

        self.frame_mos = tk.Frame(self.master_frame)
        self.frame_xrd1 = tk.Frame(self.master_frame)
        self.frame_pole_fig = tk.Frame(self.master_frame)

        self.mos_text = ScrolledText(self.frame_mos, width=70, height=40)
        self.mos_text.grid(row=0, column=0)
        self.mos_text.config(state="normal")

        self.xrd1_text = ScrolledText(self.frame_xrd1, width=70, height=40)
        self.xrd1_text.grid(row=0, column=0)
        self.xrd1_text.config(state="normal")

        self.pole_fig_text = ScrolledText(self.frame_pole_fig, width=70, height=40)
        self.pole_fig_text.grid(row=0, column=0)
        self.pole_fig_text.config(state="normal")


    def plot_XRD1(self, string_list):
        self.hide_all_plots()
        self.frame_xrd1.grid(row=0, column=0)
        self.xrd1_text.delete('1.0', "end")

        No_Chars = 12
        self.xrd1_text.insert("end", csv_to_human_readable("Angle,Intensity,Sqrt,Log,log+offs", No_Chars))
        self.xrd1_text.insert("end", "\n")
        for s in string_list:
            self.xrd1_text.insert("end", csv_to_human_readable(s, No_Chars))
            self.xrd1_text.insert("end", "\n")

    def plot_MOS(self, string_list):
        self.hide_all_plots()
        self.frame_mos.grid(row=0, column=0)
        self.mos_text.delete('1.0', "end")

        No_Chars = 12
        self.mos_text.insert("end", csv_to_human_readable("Time,First,Second,Relax,Total_T,Value", No_Chars))
        self.mos_text.insert("end", "\n")
        for s in string_list:
            self.mos_text.insert("end", csv_to_human_readable(s, No_Chars))
            self.mos_text.insert("end", "\n")

    def plot_Pole_text(self, string_list):
        self.hide_all_plots()
        self.frame_pole_fig.grid(row=0, column=0)
        self.pole_fig_text.delete('1.0', "end")

        No_Chars = 10
        self.pole_fig_text.insert("end", csv_to_human_readable("Phi,Chi,Linear,Log,Sqrt", No_Chars))
        self.pole_fig_text.insert("end", "\n")
        for s in string_list:
            self.pole_fig_text.insert("end", csv_to_human_readable(s, No_Chars))
            self.pole_fig_text.insert("end", "\n")


    def hide_all_plots(self):
        self.frame_mos.grid_forget()
        self.frame_xrd1.grid_forget()
        self.frame_pole_fig.grid_forget()
