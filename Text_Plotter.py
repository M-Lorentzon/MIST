import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from Util.csv_string_human_readable import *
import Util.Definitions as Defs

class Text_Plotter:

    def __init__(self):
        pass


    def plot_XRD1(self, string_list):

        master_frame = tk.Toplevel(bg=Defs.c_frame_color)
        frame_xrd1 = tk.Frame(master_frame)
        frame_xrd1.grid()
        xrd1_text = ScrolledText(frame_xrd1, width=70, height=58)
        xrd1_text.grid(row=0, column=0)
        xrd1_text.config(state="normal")


        No_Chars = 12
        xrd1_text.insert("end", csv_to_human_readable("Angle,Intensity,Sqrt,Log,log+offs", No_Chars))
        xrd1_text.insert("end", "\n")
        for s in string_list:
            xrd1_text.insert("end", csv_to_human_readable(s, No_Chars))
            xrd1_text.insert("end", "\n")

    def plot_MOS(self, string_list):

        master_frame = tk.Toplevel(bg=Defs.c_frame_color)
        frame_mos = tk.Frame(master_frame)
        frame_mos.grid()
        mos_text = ScrolledText(frame_mos, width=70, height=58)
        mos_text.grid(row=0, column=0)
        mos_text.config(state="normal")

        No_Chars = 12
        mos_text.insert("end", csv_to_human_readable("Time,First,Second,Relax,Total_T,Value", No_Chars))
        mos_text.insert("end", "\n")
        for s in string_list:
            mos_text.insert("end", csv_to_human_readable(s, No_Chars))
            mos_text.insert("end", "\n")

    def plot_Pole_text(self, string_list):

        master_frame = tk.Toplevel(bg=Defs.c_frame_color)
        frame_pole_fig = tk.Frame(master_frame)
        frame_pole_fig.grid()
        pole_fig_text = ScrolledText(frame_pole_fig, width=70, height=58)
        pole_fig_text.grid(row=0, column=0)
        pole_fig_text.config(state="normal")

        No_Chars = 10
        pole_fig_text.insert("end", csv_to_human_readable("Phi,Chi,Linear,Log,Sqrt", No_Chars))
        pole_fig_text.insert("end", "\n")
        for s in string_list:
            pole_fig_text.insert("end", csv_to_human_readable(s, No_Chars))
            pole_fig_text.insert("end", "\n")

