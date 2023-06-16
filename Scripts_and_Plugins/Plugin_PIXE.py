import tkinter as tk

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry

import tkscrolledframe as SF
import matplotlib.pyplot as plt
import Util.Definitions as Defs

Description = """This script is a plotting tool for PIXE-data.

First open the files you want to use and import. 

You have the option to select... and do ... in 
the script.

"""

class Plugin_PIXE:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler # to get data from

        self.active = False
        self.savable_script = False

        # Private frames
        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)  # Master within this scope

        self.sframe = SF.ScrolledFrame(self.my_frame, width=400, height=160)
        self.sframe.grid(row=11, column=0, columnspan=3)
        self.sframe.config(bg=Defs.c_frame_color)
        self.sframe.bind_arrow_keys(self.my_frame)
        self.sframe.bind_scroll_wheel(self.my_frame)
        self.label_entry_frame = self.sframe.display_widget(tk.Frame)
        self.label_entry_frame.config(bg=Defs.c_frame_color)

        self.master_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.master_button_frame.grid(row=3, column=0)
        self.select_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.select_button_frame.grid(row=4, column=0)
        self.entry_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.entry_frame.grid(row=5, column=0)
        self.calibration_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.calibration_frame.grid(row=6, column=0)

        # Master label
        self.label = tk.Label(self.my_frame, text="PIXE data settings", bg=Defs.c_script_name)
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
        self.b_plot = tk.Button(self.master_button_frame, text="Plot", command=self.callback_plot_button)
        self.b_plot.config(width=8)
        self.b_plot.grid(row=0, column=2, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files", command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=3, sticky="NW")

        # Selection buttons
        self.selection_index = 1
        self.b_linear = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=5, column=0, sticky="NW")
        self.b_log = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=5, column=1, sticky="NW")
        self.b_sqrt = tk.Button(self.select_button_frame, text="SQRT", command=self.callback_sqrt_button)
        self.b_sqrt.grid(row=5, column=2, sticky="NW")

        # Entries
        self.Entry_offset = My_Float_Entry(self.entry_frame, "Multi-graph offset", 1, 1, 0)
        self.Entry_Line_Thickn = My_Float_Entry(self.entry_frame, "Line thickness", 0.5, 1, 1)
        self.Entry_title = My_Label_Entry(self.entry_frame, "Title", 0, 0, 4)

        self.Cal_energy_offset = My_Float_Entry(self.calibration_frame, "E-Offs", 0, 0, 0)
        self.Cal_energy_per_channel = My_Float_Entry(self.calibration_frame, "E/Ch", 1, 0, 1)

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

        self.fig_stack = None
        self.ax_stack = None

        # Setup correctly
        self.callback_sqrt_button()

    def channel_to_energy(self, list_, offset, energy_per_channel):
        energy = []
        for channel in list_:
            value = offset + channel*energy_per_channel
            energy.append(value)
        return energy

    def callback_plot_button(self):
        if self.fig_stack == None:
            self.fig_stack, self.ax_stack = plt.subplots(num=105)
        self.ax_stack.cla()

        Number_of_graphs = len(self.file_data)

        for file_index in range(len(self.file_data)):
            energy = self.channel_to_energy(self.file_data[file_index].Column1, self.Cal_energy_offset.get_value(), self.Cal_energy_per_channel.get_value())
            label = self.data_labels[file_index].get_value()
            offset = self.Entry_offset.get_value() * (Number_of_graphs - file_index)
            Line_thickness = self.Entry_Line_Thickn.get_value()

            if self.selection_index == 0:  # linear
                self.ax_stack.plot(energy, self.file_data[file_index].get_col2_in_linear_with_offset(offset),
                                   label=label, linewidth=Line_thickness)
                self.ax_stack.set_ylabel("Intensity (linear, a.u)")
            elif self.selection_index == 1:  # log
                self.ax_stack.plot(energy, self.file_data[file_index].get_col2_in_log_with_offset(offset), label=label,
                                   linewidth=Line_thickness)
                self.ax_stack.set_ylabel("Intensity (log10, a.u)")
            elif self.selection_index == 2:  # sqrt
                self.ax_stack.plot(energy, self.file_data[file_index].get_col2_in_sqrt_with_offset(offset), label=label,
                                   linewidth=Line_thickness)
                self.ax_stack.set_ylabel("Intensity (sqrt, a.u)")
            else:
                print("Error in selecting lin, log or sqrt")

        self.fig_stack.suptitle(self.Entry_title.get_value())
        self.ax_stack.set_xlabel("Energy")
        self.ax_stack.legend()
        self.ax_stack.legend().set_draggable(True)

        self.fig_stack.show()

    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels :
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []

    def callback_import_all_button(self):
        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns()
            self.file_data.append(data_in_file)

            new_entry = My_Label_Entry(self.label_entry_frame, data_in_file.file_name, self.no_files_index, 0)
            new_entry.set_label_bg("seagreen1")
            new_entry.set_entry_value(data_in_file.file_name)
            self.data_labels.append(new_entry)

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns()
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def callback_linear_button(self):
        self.selection_index = 0
        self.unmark_select_buttons()
        self.b_linear.config(bg=Defs.c_button_active)

    def callback_log_button(self):
        self.selection_index = 1
        self.unmark_select_buttons()
        self.b_log.config(bg=Defs.c_button_active)

    def callback_sqrt_button(self):
        self.selection_index = 2
        self.unmark_select_buttons()
        self.b_sqrt.config(bg=Defs.c_button_active)

    def unmark_select_buttons(self):
        self.b_linear.config(bg=Defs.c_button_inactive)
        self.b_log.config(bg=Defs.c_button_inactive)
        self.b_sqrt.config(bg=Defs.c_button_inactive)

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()