import tkinter as tk
from Util.My_Float_Entry import My_Float_Entry
from Scripts_and_Plugins import Script_MOS as Script
import Util.Definitions as Defs

Description = """This script separates MOS data in multiple 
columns as received from a multilayer measurement.

-'Time layer 1 / 2': The dep. time for each layer. 
-'Time first layer': The time for absolute first
    layer. If zero, use Time layer 1.
-'Time addition second layer': An addition to 
-'Time layer 2' for second layer.
-'Rate layer 1': Dep. rate for material 1.
-'Rate layer 2': Dep. rate for material 2. 
-'Total no. of bilayers': For relaxation column,
    i.e. when no deposition is done. If =0, 
    treat the entire data file as deposition.
-'Offset thickness': Puts an addition to the layer
    thickness, e.g. if data from middle of dep.

* Required input    ** Optional input
*** Different function if not zero
"""

class MOS_Script:

    def __init__(self, Script_frame, file_handler, plotter):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler
        self.o_Text_Plotter = plotter

        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)

        self.script_active = False  # indicator of script activity

        # Label
        self.label = tk.Label(self.my_frame, text="MOS script settings", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=4)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Buttons
        self.b_calculate = tk.Button(self.my_frame, text="Calculate", command=self.callback_calculate)
        self.b_calculate.grid(row=2, column=0, sticky="NW")

        # Entries
        self.Time_1 = My_Float_Entry(self.my_frame, "Time layer 1 *", 600, 5, 0, 1)
        self.Time_2 = My_Float_Entry(self.my_frame, "Time layer 2 *", 600, 5, 1, 1)
        self.Time_F = My_Float_Entry(self.my_frame, "Time first layer**", 0, 6, 0, 1)
        self.Time_S = My_Float_Entry(self.my_frame, "Time addition second lay**", 0, 6, 1, 1)
        self.Rate_1 = My_Float_Entry(self.my_frame, "Rate layer 1**", 0, 7, 0, 1)
        self.Rate_2 = My_Float_Entry(self.my_frame, "Rate layer 2**", 0, 7, 1, 1)
        self.No_Layers = My_Float_Entry(self.my_frame, "Total no of bilayers***", 0, 8, 0, 1)
        self.Offset = My_Float_Entry(self.my_frame, "Offset thickness***", 0, 8, 1, 1)

        self.delim = ","

        # Raw data
        self.Time_col = []
        self.Val_col = []

        # Calculated data in string .csv format
        self.results = []

        # debug

    def callback_calculate(self):
        Data = self.o_file_handler.get_current_data()
        Data.extract_columns("\t")
        time_col = Data.Column1
        val_col = Data.Column2
        self.update(time_col, val_col)

        # Plot the resulting file!
        self.o_Text_Plotter.plot_MOS(self.get_results())

    def update(self, time, val):
        self.Time_col = time
        self.Val_col = val

        self.results = Script.Script_MOS(self.Time_col, self.Val_col, self.Time_1.get_value(), self.Time_2.get_value(),
                                         self.Time_F.get_value(), self.Time_S.get_value(), self.Rate_1.get_value(),
                                         self.Rate_2.get_value(), self.No_Layers.get_value(), self.Offset.get_value(),
                                         self.delim)

    def get_results(self):
        return self.results

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()



