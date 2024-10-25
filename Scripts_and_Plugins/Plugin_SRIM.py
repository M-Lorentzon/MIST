import tkinter as tk

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry

import tkscrolledframe as SF
import matplotlib.pyplot as plt
import Util.Definitions as Defs

Description = """This script is a plotting tool for stacked lines
especially for XRD data (.xy files).

First open the files you want to use and import 

"""

class Plugin_SRIM:

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
        self.entry_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1,
                                    bg=Defs.c_script_entries)
        self.entry_frame.grid(row=5, column=0)

        # Master label
        self.label = tk.Label(self.my_frame, text="SRIM output data settings", bg=Defs.c_script_name)
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
        self.selection_index_X = 1
        self.label_X = tk.Label(self.select_button_frame, text="X-axis", bg=Defs.c_script_name)
        self.label_X.grid(row=5, column=0)
        self.label_X.config(font=('Helvetica', 11))
        self.b_linear_X = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button_X)
        self.b_linear_X.grid(row=5, column=1, sticky="NW")
        self.b_log_X = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button_X)
        self.b_log_X.grid(row=5, column=2, sticky="NW")

        self.Entry_Line_Thickn = My_Float_Entry(self.entry_frame, "Graph line thickness", 0.5, 1, 1)
        self.e_xlim_min = My_Float_Entry(self.entry_frame, "xlim min, 10^_", 3, 2, 0)
        self.e_xlim_max = My_Float_Entry(self.entry_frame, "xlim max, 10^_", 9, 2, 1)
        self.e_ylim_min = My_Float_Entry(self.entry_frame, "ylim min, 10^_", -4, 3, 0)
        self.e_ylim_max = My_Float_Entry(self.entry_frame, "ylim max, 10^_", 4, 3, 1)

        self.selection_index_Y = 1
        self.label_Y = tk.Label(self.select_button_frame, text="Y-axis", bg=Defs.c_script_name)
        self.label_Y.grid(row=6, column=0)
        self.label_Y.config(font=('Helvetica', 11))
        self.b_linear_Y = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button_Y)
        self.b_linear_Y.grid(row=6, column=1, sticky="NW")
        self.b_log_Y = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button_Y)
        self.b_log_Y.grid(row=6, column=2, sticky="NW")

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

        self.fig_stack = None
        self.ax_stack = None

        # Setup correctly
        self.callback_log_button_X()
        self.callback_log_button_Y()

    def on_close(self, event):
        print("closed window")
        self.fig_stack = None
        self.ax_stack = None

    def callback_plot_button(self):
        # First time opening the plot -> Initialize it!
        if self.fig_stack == None:
            self.fig_stack, self.ax_stack = plt.subplots(num=100)
            self.fig_stack.canvas.mpl_connect('close_event', self.on_close)

        self.ax_stack.cla()
        Line_thickness = self.Entry_Line_Thickn.get_value()

        for file_index in range(len(self.file_data)):
            energy = self.file_data[file_index].Column1
            electronic_stopping = self.file_data[file_index].Column2
            nuclear_stopping = self.file_data[file_index].Column3
            sum_stopping = self.file_data[file_index].Column4
            name =  self.data_labels[file_index].get_value()


            self.ax_stack.plot(energy, electronic_stopping, label=name+" Electronic", linewidth=Line_thickness)
            self.ax_stack.plot(energy, nuclear_stopping, label=name+" Nuclear", linewidth=Line_thickness)
            self.ax_stack.plot(energy, sum_stopping, label=name+" Sum", linewidth=Line_thickness)

            if self.selection_index_Y == 0:
                self.ax_stack.set_yscale("linear")
            elif self.selection_index_Y == 1:
                self.ax_stack.set_yscale("log")

            if self.selection_index_X == 0:
                self.ax_stack.set_xscale("linear")
            elif self.selection_index_X == 1:
                self.ax_stack.set_xscale("log")

            min_power_x = self.e_xlim_min.get_value()
            max_power_x = self.e_xlim_max.get_value()
            min_power_y = self.e_ylim_min.get_value()
            max_power_y = self.e_ylim_max.get_value()
            self.ax_stack.set_xlim([10**min_power_x, 10**max_power_x])
            self.ax_stack.set_ylim([10 ** min_power_y, 10 ** max_power_y])


            self.fig_stack.suptitle(self.file_data[file_index].get_name())
            self.ax_stack.set_ylabel("Stopping Power")
            self.ax_stack.set_xlabel("Ion energy [eV]")
            self.ax_stack.legend()
            self.ax_stack.legend().set_draggable(True)
            self.fig_stack.show()


    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels:
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []

    def callback_import_all_button(self):
        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns_SRIM()
            self.file_data.append(data_in_file)

            new_entry = My_Label_Entry(self.label_entry_frame, data_in_file.file_name, self.no_files_index, 0)
            new_entry.set_label_bg("seagreen1")
            new_entry.set_entry_value(data_in_file.file_name)
            self.data_labels.append(new_entry)

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns_SRIM()
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def callback_linear_button_X(self):
        self.selection_index_X = 0
        self.unmark_select_buttons_X()
        self.b_linear_X.config(bg=Defs.c_button_active)

    def callback_log_button_X(self):
        self.selection_index_X = 1
        self.unmark_select_buttons_X()
        self.b_log_X.config(bg=Defs.c_button_active)

    def callback_linear_button_Y(self):
        self.selection_index_Y = 0
        self.unmark_select_buttons_Y()
        self.b_linear_Y.config(bg=Defs.c_button_active)

    def callback_log_button_Y(self):
        self.selection_index_Y = 1
        self.unmark_select_buttons_Y()
        self.b_log_Y.config(bg=Defs.c_button_active)

    def unmark_select_buttons_X(self):
        self.b_linear_X.config(bg=Defs.c_button_inactive)
        self.b_log_X.config(bg=Defs.c_button_inactive)

    def unmark_select_buttons_Y(self):
        self.b_linear_Y.config(bg=Defs.c_button_inactive)
        self.b_log_Y.config(bg=Defs.c_button_inactive)

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()