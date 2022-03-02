import tkinter as tk
from Util.My_Float_Entry import My_Float_Entry

Description = """This script treats ___ data
and produce _____ 

"""

class Plugin_Template:

    def __init__(self, Script_frame):
        self.script_frame = Script_frame # shared with all scripts

        self.my_frame = tk.Frame(self.script_frame)

        self.script_active = False  # indicator of script activity

        # Label
        self.label = tk.Label(self.my_frame, text="Template script settings")
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Text
        self.text = tk.Text(self.my_frame, width=40, height=15)
        self.text.grid(row=1, column=0)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Entries
        self.Entry____ = My_Float_Entry(self.my_frame, "___", 600, 2, 0)

        self.delim = ","

        # Raw data
        self.Angle_Col = []
        self.Intensity_col = []

        # Calculated data in string .csv format
        self.results = []



    def update(self, Angle, intensity):
        self.Angle_Col = Angle
        self.Intensity_col = intensity

        # Update results with list of strings.
        # self.results = 'script function'

    def get_results(self):
        return self.results

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()



