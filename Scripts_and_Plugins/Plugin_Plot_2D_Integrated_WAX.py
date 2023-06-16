
import tkinter as tk

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
import Util.Definitions as Defs

import tkscrolledframe as SF
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

Description = """This script is a plotting tool for stacked lines
from the output of WAX data integration 

First open the files you want to use and import 
    """

class Plugin_Plot_2D_Integrated_WAX:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame  # shared with all scripts
        self.o_file_handler = file_handler  # to get data from

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
        self.label = tk.Label(self.my_frame, text="XRD stacked lines settings", bg=Defs.c_script_name)
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

        # Selections
        self.selection_index = 0 # 0 = linear, 1 = log
        self.b_linear = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=2, column=0, sticky="NW")
        self.b_log = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=2, column=1, sticky="NW")

        self.selection_integrate_axis = 0  # 0 = tth, 1 = d_hkl
        self.b_select_tth = tk.Button(self.select_button_frame, text="2\u03B8 [\u00B0]", command=self.callback_select_axis_tth)
        self.b_select_tth.grid(row=2, column=2, sticky="NW")
        self.b_select_d_hkl = tk.Button(self.select_button_frame, text="d\u2095\u2096\u2097", command=self.callback_select_axis_d_hkl)
        self.b_select_d_hkl.grid(row=2, column=3, sticky="NW")
        self.callback_select_axis_tth()

        self.b_legend = tk.Button(self.select_button_frame, text="legend", command=self.callback_enable_legend)
        self.b_legend.grid(row=2, column=4)
        self.legend_enabled = True
        self.callback_enable_legend()

        # Entries
        self.e_beam_energy = My_Float_Entry(self.entry_frame, "X-ray energy", 73.8, 0, 0)
        self.e_plot_offset = My_Float_Entry(self.entry_frame, "Plot offset", 1000, 0, 1)

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

        self.fig_stack = None
        self.ax_stack = None

    def on_close(self, event):
        print("closed window")
        self.fig_stack = None
        self.ax_stack = None

    def callback_plot_button(self):
        # First time opening the plot -> Initialize it!
        if self.fig_stack is None:
            self.fig_stack, self.ax_stack = plt.subplots(num=Defs.fig_2d_WAX_output)
            self.fig_stack.canvas.mpl_connect('close_event', self.on_close)

        self.ax_stack.cla()

        Number_of_graphs = len(self.file_data)
        cmap = cm.get_cmap('jet', Number_of_graphs)

        for index in range(Number_of_graphs):
            file = self.file_data[index]

            intensity = file.get_col2_in_linear_with_offset(index*self.e_plot_offset.get_value())
            Tth = np.array(file.Column1)
            d_space = self.get_wavelength() * 1e10 / (2 * np.sin(np.radians(Tth / 2)))

            #########
            if self.selection_integrate_axis == 0: # tth
                self.ax_stack.plot(Tth, intensity, label=self.data_labels[index].get_value(),
                                   marker="o", linestyle="--", alpha=0.4, markersize=4, color=cmap(index))
                self.ax_stack.set_xlabel(r"$2\mathrm{\theta \ (^o)} $ ")

            elif self.selection_integrate_axis == 1: # d_hkl
                self.ax_stack.plot(d_space, intensity, label=self.data_labels[index].get_value(),
                                   marker="o", linestyle="--", alpha=0.4, markersize=4, color=cmap(index))
                self.ax_stack.set_xlabel("d\u2095\u2096\u2097 [Å]")

            #########
            if self.selection_index == 0:  # Linear
                self.ax_stack.set_yscale('linear')
                self.ax_stack.set_ylabel("Intensity (arb. unit)")

            elif self.selection_index == 1:  # Log
                self.ax_stack.set_yscale('log')
                self.ax_stack.set_ylabel("Log intensity (arb. unit)")

        if self.legend_enabled:
            self.ax_stack.legend()
            self.ax_stack.legend().set_draggable(True)

        self.fig_stack.show()

    def get_wavelength(self):
        # Energy should be in keV !!!
        # Return the wavelenght in m
        # -----------------------------------
        energy = self.e_beam_energy.get_value()

        # Plank Constant
        h = 6.62607004e-34  # m2 . kg / s
        # light celerity
        c = 299792458  # m / s
        # Joule -> eV
        eV = 6.242e+18  # eV / J

        # Conversion Energy -> wavelenght
        wavelenght = ((h * c) / (energy * 1e3 / eV))  # m

        return wavelenght

    def callback_linear_button(self):
        self.selection_index = 0
        self.unmark_select_buttons()
        self.b_linear.config(bg=Defs.c_button_active)

    def callback_log_button(self):
        self.selection_index = 1
        self.unmark_select_buttons()
        self.b_log.config(bg=Defs.c_button_active)

    def unmark_select_buttons(self):
        self.b_linear.config(bg=Defs.c_button_inactive)
        self.b_log.config(bg=Defs.c_button_inactive)

    def callback_select_axis_tth(self):
        self.selection_integrate_axis = 0
        self.unmark_axis_selection()
        self.b_select_tth.config(bg=Defs.c_button_active)

    def callback_select_axis_d_hkl(self):
        self.selection_integrate_axis = 1
        self.unmark_axis_selection()
        self.b_select_d_hkl.config(bg=Defs.c_button_active)

    def unmark_axis_selection(self):
        self.b_select_tth.config(bg=Defs.c_button_inactive)
        self.b_select_d_hkl.config(bg=Defs.c_button_inactive)

    def callback_enable_legend(self):
        if self.legend_enabled:
            self.legend_enabled = False
            self.b_legend.config(bg=Defs.c_button_inactive)
        else:
            self.legend_enabled = True
            self.b_legend.config(bg=Defs.c_button_active)

    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels :
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []
        plt.clf()

    def callback_import_all_button(self):
        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns_2D_WAX(23)
            self.file_data.append(data_in_file)

            new_entry = My_Label_Entry(self.label_entry_frame, data_in_file.file_name, self.no_files_index, 0)
            new_entry.set_label_bg("seagreen1")
            new_entry.set_entry_value(data_in_file.file_name)
            self.data_labels.append(new_entry)

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns_2D_WAX(23)
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()