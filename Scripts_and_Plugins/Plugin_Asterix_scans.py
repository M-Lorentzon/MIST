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
import Util.List_Of_Strings_Container as string_cont

Description = """This script is a tool for plotting "normal" scans
from Asterix file formats

"""

class Plugin_Asterix_scans:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler # to get data from

        self.active = False
        self.savable_script = False

        # Private frames
        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)  # Master within this scope

        self.master_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.master_button_frame.grid(row=2, column=0)
        self.select_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.select_button_frame.grid(row=3, column=0)
        self.entry_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.entry_frame.grid(row=8, column=0)

        self.plot_selection_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.plot_selection_frame.grid(row=5, column=0)
        self.calculate_new_file_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.calculate_new_file_frame.grid(row=6, column=0)

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
        self.b_calculate_and_save =tk.Button(self.master_button_frame, text="Calc. & save", command=self.callback_calculate_and_save_new_file)
        self.b_calculate_and_save.config(width=12)
        self.b_calculate_and_save.grid(row=0, column=5, sticky="NW")


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

        self.Entry_offset = My_Float_Entry(self.entry_frame, "Multi-graph offset", 0, 1, 0)
        self.Entry_offset.set_entry_width(10)
        self.Entry_Line_Thickn = My_Float_Entry(self.entry_frame, "Graph line thickness", 0.5, 1, 1)
        self.Entry_title = My_Label_Entry(self.entry_frame, "Title", 0, 0, 4)

        self.e_calc_background_intensity = My_Float_Entry(self.calculate_new_file_frame, "Background intensity", 0, 1, 0)
        self.e_calc_center_omega = My_Float_Entry(self.calculate_new_file_frame, "Omega Center", 0, 1, 1)

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_tuple = []
        self.label_container = SF_cont.My_SF_Selection_Entry_Container(self.my_frame, 400, 200, 10, 0)

        # Plotting objects and settings
        self.fig = None
        self.ax = None


    def on_close(self, event):
        self.fig = None
        self.ax = None

    def add_offset_to_list(self, original, offset):
        ret_list = []
        for element in original:
            ret_list.append(element + offset)
        return ret_list


    def callback_plot_button(self):

        if self.fig is None:
            self.fig, self.ax = plt.subplots(num=Defs.fig_asterix_scans)
            self.fig.canvas.mpl_connect('close_event', self.on_close)

        self.ax.cla()


        number_of_graphs = len(self.file_tuple)
        offset_single = self.Entry_offset.get_value()
        Line_thickness = self.Entry_Line_Thickn.get_value()

        for ix in range(number_of_graphs):

            touple = self.file_tuple[ix]

            label = self.label_container.get_entry_value(ix)
            omega = touple[0]
            intensity = touple[1]

            self.ax.plot(omega, self.add_offset_to_list(intensity, offset_single*(ix+1)), label=label)


        ### Customizations ###
        if self.plot_selection_index == 0: # linear
            self.ax.set_yscale('linear')
        elif self.plot_selection_index == 1: # log
            self.ax.set_yscale('log')
        else:
            print("Error in plotting, selection index...")

        self.ax.legend()
        self.ax.legend().set_draggable(True)

        self.fig.show()

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

    def callback_calculate_and_save_new_file(self):
        new_omega = []
        new_intensity = []
        file_index = self.label_container.index_current_highlight
        file_name = self.label_container.get_selected_entry().get_value() + "_converted"
        if file_index < 0:
            print("need file...")
            return

        old_omega = self.file_tuple[self.label_container.index_current_highlight][0]
        old_intensity = self.file_tuple[self.label_container.index_current_highlight][1]

        for element in old_omega:
            new_omega.append(element - self.e_calc_center_omega.get_value())

        for element in old_intensity:
            new_intensity.append(element - self.e_calc_background_intensity.get_value())

        string_container = string_cont.List_Of_Strings_Container()
        for ix in range(len(new_intensity)):
            string_container.add_row_2(new_omega[ix], new_intensity[ix], 4, " ")


        self.o_file_handler.save_file(string_container.String_List, file_name)

    def extract_file_data(self, data_container):
        Raw_Data = data_container.list_of_lines

        first_angle = float(re.split(',', Raw_Data[18])[1])
        scan_range = float(re.split(',', Raw_Data[19])[1])
        step_width = float(re.split(',', Raw_Data[20])[1])
        time_per_step = float(re.split(',', Raw_Data[21])[1])

        min_data_index = 24
        data_points = float(re.split(',', Raw_Data[22])[1])
        file_name = re.split(',', Raw_Data[0])[1]

        wavelength = float(re.split(',', Raw_Data[6])[1])
        twotheta = float(re.split(',', Raw_Data[11])[1])

        intensities = []
        omega_angles = []

        for ix in range(int(data_points)):
            intensity = float(Raw_Data[ix + min_data_index])
            omega_angle = first_angle + (ix * step_width)

            intensities.append(intensity)
            omega_angles.append(omega_angle)

        self.file_tuple.append((omega_angles, intensities))
        self.label_container.add_entry(data_container.file_name)
        self.label_container.highlight_active_file()

        #print(self.file_touple)


    def callback_import_button(self):
        # Import raw data from data_container since this is an atypical data storage.
        # I.e. treat it differently from other scripts...

        self.no_files_index += 1
        data_container = self.o_file_handler.get_current_data()
        self.extract_file_data(data_container)



    def callback_import_all_button(self):
        for data_container in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            self.extract_file_data(data_container)


    def callback_clear_files_button(self):
        self.file_tuple.clear()
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