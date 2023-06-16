import tkinter as tk
import Util.Definitions as Defs
import math as math
from Util.My_Float_Entry import My_Float_Entry
from tkinter.scrolledtext import ScrolledText
from Scripts_and_Plugins.Calculations_Scripts.Calculate_angle_between_hexagonal_planes import *
from Scripts_and_Plugins.Calculations_Scripts.Calculate_angle_between_cubic_planes import *

Description = """This script is used for calculations
of frequent equations. 
For example: 
* Lattice parameters
* Density (from composition and lattice param)
* ... 

"""

class Plugin_Material_Calc:

    def __init__(self, Script_frame):
        self.script_frame = Script_frame # shared with all scripts

        self.active = False
        self.savable_script = False

        self.my_frame = tk.Frame(self.script_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)

        # Label
        self.label = tk.Label(self.my_frame, text="Material parameter calculations", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Frames
        self.calculation_selection_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.calculation_selection_frame.grid(row=2, column=0)
        self.lattice_param_calc_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.Hexagonal_angle_calculation_frame =  tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.Cubic_angle_calculation_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.display_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.display_frame.grid(row=4, column=0)

        # Selection buttons
        self.b_lattice_param = tk.Button(self.calculation_selection_frame, text="Lat param", command=self.callback_lattice_button)
        self.b_lattice_param.grid(row=0, column=0, sticky="NW")

        self.b_hex_calc = tk.Button(self.calculation_selection_frame, text="Hex angles", command=self.callback_hexagonal_angles_button)
        self.b_hex_calc.grid(row=0, column=1, sticky="NW")
        self.b_cub_calc = tk.Button(self.calculation_selection_frame, text="Cube angles", command=self.callback_cubic_angles_button)
        self.b_cub_calc.grid(row=0, column=2, sticky="NW")

        # Result text and other stuff for results
        self.result_text = ScrolledText(self.display_frame, width=45, height=8)
        self.result_text.grid(row=0, column=0, columnspan=5)
        self.result_text.insert(0.0, "Calculated results: ")
        self.result_text.config(state='normal')
        self.line_index = 0

        ### Lattice Calculation stuff ###
        self.latt_button_calc = tk.Button(self.lattice_param_calc_frame, text="Calculate", command=self.latt_callback_calculate)
        self.latt_button_calc.config(width=8)
        self.latt_button_calc.grid(row=1, column=0, sticky="NW")
        self.latt_label = tk.Label(self.lattice_param_calc_frame, text="Cubic lattice", bg=Defs.c_script_name)
        self.latt_label.grid(row=1, column=1)
        self.latt_label.config(font=('Helvetica', 11))

        self.latt_miller_h = My_Float_Entry(self.lattice_param_calc_frame, " h: ", 0, 2, 0)
        self.latt_miller_k = My_Float_Entry(self.lattice_param_calc_frame, " k: ", 0, 2, 1)
        self.latt_miller_l = My_Float_Entry(self.lattice_param_calc_frame, " l: ", 2, 2, 2)
        self.latt_wavelength = My_Float_Entry(self.lattice_param_calc_frame, "Lambda [Å]:", 1.5406, 3, 0)
        self.latt_2theta = My_Float_Entry(self.lattice_param_calc_frame, " 2Theta: ", 12.34, 3, 1)

        ### Calculation scripts
        self.o_calculate_angle_hexagonal = calculate_angle_between_hexagonal_planes(self.print_results, self.Hexagonal_angle_calculation_frame)
        self.o_calculate_angle_cubic = calculate_angle_between_cubic_planes(self.print_results, self.Cubic_angle_calculation_frame)

        ### General stuff ###
        self.selection_index = 0 # 0=lattice, 1=vector
        self.callback_lattice_button()

    def callback_hexagonal_angles_button(self):
        self.selection_index = 1
        self.ungrid_sub_calc_frames()
        self.Hexagonal_angle_calculation_frame.grid(row=3, column=0)
        self.unmark_select_buttons()
        self.b_hex_calc.config(bg=Defs.c_button_active)

    def callback_cubic_angles_button(self):
        self.selection_index = 1
        self.ungrid_sub_calc_frames()
        self.Cubic_angle_calculation_frame.grid(row=3, column=0)
        self.unmark_select_buttons()
        self.b_cub_calc.config(bg=Defs.c_button_active)

    def callback_lattice_button(self):
        self.selection_index = 0
        self.ungrid_sub_calc_frames()
        self.lattice_param_calc_frame.grid(row=3, column=0)
        self.unmark_select_buttons()
        self.b_lattice_param.config(bg=Defs.c_button_active)

    def latt_callback_calculate(self):
        wavelen = self.latt_wavelength.get_value()
        mill_h = self.latt_miller_h.get_value()
        mill_k = self.latt_miller_k.get_value()
        mill_l = self.latt_miller_l.get_value()
        twotheta = self.latt_2theta.get_value()
        d_space = wavelen / (2 * math.sin(math.radians(twotheta/2)))
        lattice_param = d_space * math.sqrt(mill_h**2 + mill_k**2 + mill_l**2)
        self.print_results("d="+str(d_space))
        self.print_results("a=" + str(lattice_param))


    #### Help-functions #######
    def ungrid_sub_calc_frames(self):
        self.lattice_param_calc_frame.grid_forget()
        self.Hexagonal_angle_calculation_frame.grid_forget()
        self.Cubic_angle_calculation_frame.grid_forget()

    def unmark_select_buttons(self):
        self.b_lattice_param.config(bg=Defs.c_button_inactive)
        self.b_hex_calc.config(bg=Defs.c_button_inactive)
        self.b_cub_calc.config(bg=Defs.c_button_inactive)

    def print_results(self, line):
        self.line_index += 1
        self.result_text.insert("end", "\n")
        self.result_text.insert("end", str(self.line_index)+": ", 'line')
        self.result_text.insert("end", line, 'text')
        self.result_text.tag_config('text', foreground='black')
        self.result_text.tag_config('line', foreground='green')
        self.result_text.yview('end')
##################################################

    def update(self, Angle, intensity):
        pass

    def get_results(self):
        pass

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()



