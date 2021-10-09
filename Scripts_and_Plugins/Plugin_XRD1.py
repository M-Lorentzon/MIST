import tkinter as tk
from Util.My_Float_Entry import My_Float_Entry
import Util.Definitions as Defs
from Scripts_and_Plugins.Script_XRD1 import *

Description = """This script treats XRD data or any data which
consists of two columns for further use in 
another plotting software e.g. Origin. 

The first column of the data is copied while the 
second column (i.e. intensity) is both copied and 
subject to calculations. 

The produced data consists of 5 columns,
Angle (copied col1), Intensity (copied col2),
Sqrt (of col2), log (of col2) and 
log+offset (of col2). 

The activated file is used for calculations.
You must press 'Calculate' before saving the 
new file 

"""

class Plugin_XRD1:

    def __init__(self, Script_frame, file_handler, plotter):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler
        self.o_Text_Plotter = plotter

        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)

        self.script_active = False  # indicator of script activity

        # Label
        self.label = tk.Label(self.my_frame, text="  XRD1 script settings  ", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Buttons
        self.b_calculate = tk.Button(self.my_frame, text="Calculate", command=self.callback_calculate)
        self.b_calculate.grid(row=2, column=0, sticky="NW")

        # Entries
        self.E_col_offset = My_Float_Entry(self.my_frame, "log val offset", 0, 3, 0)

        self.delim = ","

        # Raw data
        self.Angle_Col = []
        self.Intensity_col = []

        # Calculated data in string .csv format
        self.results = []

        # debug

    def callback_calculate(self):
        Data = self.o_file_handler.get_current_data()
        Data.extract_columns(" ")
        angle_col = Data.Column1
        intensity_col = Data.Column2
        self.update(angle_col, intensity_col)

        # Plot the resulting file!
        self.o_Text_Plotter.plot_XRD1(self.get_results())

    def update(self, Angle, intensity):
        self.Angle_Col = Angle
        self.Intensity_col = intensity

        # Update results with list of strings.
        self.results = Script_XRD1(self.Angle_Col, self.Intensity_col, self.E_col_offset.get_value(), self.delim)

    def get_results(self):
        return self.results

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()



