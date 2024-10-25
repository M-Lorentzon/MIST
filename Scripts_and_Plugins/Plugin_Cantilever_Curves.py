import math
import re
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import tkscrolledframe as SF

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry


import Util.Definitions as Defs
import Util.My_SF_Selection_Entry_Container as SF_cont

Description = """This script is a tool for plotting load-deflection
curves from cantilever. 

Also to save data in a better format. 

"""

class Plugin_Cantilever_Curves:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler # to get data from

        self.active = False
        self.savable_script = False

        # Private frames
        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)  # Master within this scope

        self.master_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.master_button_frame.grid(row=3, column=0)
        self.select_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.select_button_frame.grid(row=4, column=0)
        self.entry_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.entry_frame.grid(row=6, column=0)

        self.plot_selection_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.plot_selection_frame.grid(row=5, column=0)

        # Master label
        self.label = tk.Label(self.my_frame, text="XRD Asterix", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Master description text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Master Buttons
        self.b_import = tk.Button(self.master_button_frame, text="Import", command=self.callback_import_button)
        self.b_import.config(width=8)
        self.b_import.grid(row=0, column=0, sticky="NW")
        self.b_import_all = tk.Button(self.master_button_frame, text="Import All", command=self.callback_import_all_button)
        self.b_import_all.config(width=8)
        self.b_import_all.grid(row=0, column=1, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files", command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=2, sticky="NW")
        self.b_plot = tk.Button(self.master_button_frame, text="Plot", command=self.callback_plot_button)
        self.b_plot.config(width=8)
        self.b_plot.grid(row=0, column=4, sticky="NW")
        self.b_save_new_file = tk.Button(self.master_button_frame, text="Save file", command=self.callback_save_new_file_button)
        self.b_save_new_file.config(width=8)
        self.b_save_new_file.grid(row=0, column=5, sticky="NW")

        # Selection buttons
        self.plot_selection_index = 1
        self.b_linear = tk.Button(self.plot_selection_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=0, column=0, sticky="NW")
        self.b_linear.config(width=8)
        self.b_log = tk.Button(self.plot_selection_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=0, column=1, sticky="NW")
        self.b_log.config(width=8)
        self.callback_linear_button()  # Start with Linear as default!

        self.flip_status = 0  # 0=normal, 1=flipped
        self.b_flip_stack = tk.Button(self.select_button_frame, text="Flip", command=self.callback_flip_button)
        self.b_flip_stack.grid(row=5, column=3, sticky="NW")

        self.b_legend = tk.Button(self.select_button_frame, text="legend", command=self.callback_enable_legend)
        self.b_legend.grid(row=5, column=4)
        self.legend_enabled = True
        self.callback_enable_legend()

        self.b_black_lines = tk.Button(self.select_button_frame, text="black lines", command=self.callback_black_lines)
        self.b_black_lines.grid(row=5, column=5)
        self.use_black_lines = True
        self.callback_black_lines()

        self.Entry_title = My_Label_Entry(self.entry_frame, "Title", 0, 0, 4)
        self.Entry_max_diff = My_Float_Entry(self.entry_frame, "max_diff, end point", 5, 1, 0)
        self.Entry_start_val = My_Float_Entry(self.entry_frame, "Start val", 3.2, 1, 1)

        self.e_xlim_min = My_Float_Entry(self.entry_frame, "xlim min", 0, 2, 0)
        self.e_xlim_max = My_Float_Entry(self.entry_frame, "xlim max", 2000, 2, 1)
        self.e_ylim_min = My_Float_Entry(self.entry_frame, "ylim min", 0, 2, 2)
        self.e_ylim_max = My_Float_Entry(self.entry_frame, "ylim max", 100, 2, 3)

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.label_container = SF_cont.My_SF_Selection_Entry_Container(self.my_frame, 400, 200, 10, 0)

        # Plotting objects and settings
        self.fig = None
        self.ax = None


    def on_close(self, event):
        self.fig = None
        self.ax = None


    def find_start_and_end_points(self, list, max_diff, start_val):

        ret_ix_list = []
        # find start index!
        for ix, val in enumerate(list):
            if val > start_val:
                ret_ix_list.append(ix)
                break

        # find end fracture index!
        prev_val = list[0]
        for ix, val in enumerate(list):
            diff = abs(prev_val - val)
            if diff > max_diff:
                ret_ix_list.append(ix)
                break
            prev_val = val

        if len(ret_ix_list) == 0:
            ret_ix_list.append(0)
        if len(ret_ix_list) == 1:
            ret_ix_list.append(-1)

        return ret_ix_list

    def offset_list(self, list, offset):
        ret_list = []
        for element in list:
            ret_list.append(element - offset)
        return ret_list

    def callback_black_lines(self):
        if self.use_black_lines:
            self.use_black_lines = False
            self.b_black_lines.config(bg=Defs.c_button_inactive)
        else:
            self.use_black_lines = True
            self.b_black_lines.config(bg=Defs.c_button_active)

    def get_area(self, line):
        line_list = re.split('\t', line)
        if line_list[0] == "Area":
            return float(line_list[1])
        else:
            return 0 # default

    def calculate_stress(self, load_list, area): # area is in meters. Elements are in uN.
        ret_list = []
        if area == 0:
            return load_list
        else:
            for element in load_list:
                ret_list.append((element / 1000000 / area) / 1000000)
            return ret_list # Stress in MPa!

    def callback_plot_button(self):

        if self.fig is None:
            self.fig, self.ax = plt.subplots(num=Defs.fig_cantilever)
            self.fig.canvas.mpl_connect('close_event', self.on_close)

        self.ax.cla()

        is_stress = True
        number_of_graphs = len(self.file_data)
        for ix in range(number_of_graphs):

            depth = self.file_data[ix].Column1
            load  = self.file_data[ix].Column2

            area_line  = self.file_data[ix].list_of_lines[3]
            area = self.get_area(area_line) # 1 = default
            if area == 0: #at least one curve does not have defined area...
                is_stress = False


            ix_vals = self.find_start_and_end_points(load, self.Entry_max_diff.get_value(), self.Entry_start_val.get_value())

            good_depth = depth[ix_vals[0]:ix_vals[1]]
            good_load  = load[ix_vals[0]:ix_vals[1]]
            actual_depth = self.offset_list(good_depth, good_depth[0])
            stress = self.calculate_stress(good_load, area)

            label = self.label_container.get_entry_value(ix)
            self.ax.plot(actual_depth, stress, label=label)


        ### Customizations ###
        self.ax.set_xlim([self.e_xlim_min.get_value(), self.e_xlim_max.get_value()])
        self.ax.set_ylim([self.e_ylim_min.get_value(), self.e_ylim_max.get_value()])


        if self.plot_selection_index == 0: # linear
            self.ax.set_yscale('linear')
        elif self.plot_selection_index == 1: # log
            self.ax.set_yscale('log')
        else:
            print("Error in plotting, selection index..."),

        self.fig.suptitle(self.Entry_title.get_value())
        self.ax.set_xlabel("Displacement [nm]")
        if is_stress:
            self.ax.set_ylabel("Stress [MPa]")
        else:
            self.ax.set_ylabel("Load [\u00b5n] or other...")


        if self.legend_enabled:
            self.ax.legend()
            self.ax.legend().set_draggable(True)

        if self.use_black_lines:
            for line in self.ax.get_lines():
                line.set_color('black')

        self.fig.show()

    def callback_save_new_file_button(self):
        print("New file")


    def callback_flip_button(self):
        Prev_Status = self.flip_status
        if Prev_Status == 0:
            self.flip_status = 1
            self.b_flip_stack.config(bg=Defs.c_button_active)

        else:
            self.flip_status = 0
            self.b_flip_stack.config(bg=Defs.c_button_inactive)

    def callback_enable_legend(self):
        if self.legend_enabled:
            self.legend_enabled = False
            self.b_legend.config(bg=Defs.c_button_inactive)
        else:
            self.legend_enabled = True
            self.b_legend.config(bg=Defs.c_button_active)




    def callback_import_button(self):
        # Import raw data from data_container since this is an atypical data storage.
        # I.e. treat it differently from other scripts...

        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns(4)
        self.file_data.append(data)

        self.label_container.add_entry(data.file_name)


    def callback_import_all_button(self):

        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns(4)
            self.file_data.append(data_in_file)

            self.label_container.add_entry(data_in_file.file_name)

    def callback_clear_files_button(self):
        (self.file_data.clear())
        self.label_container.remove_all_entries()
        self.no_files_index = 0

    def callback_linear_button(self):
        self.plot_selection_index = 0
        self.unmark_select_buttons()
        self.b_linear.config(bg=Defs.c_button_active)

    def callback_log_button(self):
        self.plot_selection_index = 1
        self.unmark_select_buttons()
        self.b_log.config(bg=Defs.c_button_active)

    def unmark_select_buttons(self):
        self.b_linear.config(bg=Defs.c_button_inactive)
        self.b_log.config(bg=Defs.c_button_inactive)


    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()