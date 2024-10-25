import tkinter as tk
import math as math

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry

import tkscrolledframe as SF
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
import Util.Definitions as Defs
import numpy as np

from pathlib import Path
import webbrowser as webbrowser

Description = """This script is a plotting tool plasma probe 
measurements.

First open the files you want to use and import 

"""

class Plugin_Plasma_probe:

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

        self.Area_probe_calc_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.Area_probe_calc_frame.grid(row=7, column=0)
        self.Langmuir_probe_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.Langmuir_probe_frame.grid(row=9, column=0)

        self.Display_results_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.Display_results_frame.grid(row=10, column=0)

        # Master label
        self.label = tk.Label(self.my_frame, text="Plasma Probe Data", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Master description text
        self.text = tk.Text(self.my_frame, width=50, height=15, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Master Buttons
        self.b_import = tk.Button(self.master_button_frame, text="Import", command=self.callback_import_button)
        self.b_import.config(width=8)
        self.b_import.grid(row=0, column=0, sticky="NW")
        self.b_import_all = tk.Button(self.master_button_frame, text="Import all", command=self.callback_import_all_button)
        self.b_import_all.config(width=8)
        self.b_import_all.grid(row=0, column=1, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files", command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=2, sticky="NW")
        self.b_plot = tk.Button(self.master_button_frame, text="Plot", command=self.callback_plot_button)
        self.b_plot.config(width=8)
        self.b_plot.grid(row=0, column=4, sticky="NW")
        self.b_plasma_help = tk.Button(self.master_button_frame, text="Help Plasma", command=self.callback_help_button)
        self.b_plasma_help.config(width=8)
        self.b_plasma_help.grid(row=0, column=5, sticky="NW")

        # Result text and other stuff for results
        self.result_text = ScrolledText(self.Display_results_frame, width=45, height=8)
        self.result_text.grid(row=0, column=0, columnspan=5)
        self.result_text.insert(0.0, "Calculated results: ")
        self.result_text.config(state='normal')
        self.line_index = 0

        # Selection buttons
        self.plot_selection_index = 1
        self.b_linear = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=0, column=0, sticky="NW")
        self.b_linear.config(width=8)
        self.b_log = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=0, column=1, sticky="NW")
        self.b_log.config(width=8)
        self.callback_linear_button()  # Start with Linear as default!

        ## Area probe calculations
        self.b_calc_ion_atom_ratio = tk.Button(self.Area_probe_calc_frame, text="Calculate Ion/atom ratio", command=self.callback_calc_ion_ratio_button)
        self.b_calc_ion_atom_ratio.config(width=20)
        self.b_calc_ion_atom_ratio.grid(row=1, column=0, sticky="NW")

        self.b_draw_v_line = tk.Button(self.Area_probe_calc_frame, text="Draw v-line", command=self.callback_draw_vline_button)
        self.b_draw_v_line.config(width=8)
        self.b_draw_v_line.grid(row=0, column=0, sticky="NW")
        self.e_vline_pos = My_Float_Entry(self.Area_probe_calc_frame, "vline pos", -30, 0, 1)
        self.b_draw_h_line = tk.Button(self.Area_probe_calc_frame, text="Draw h-line", command=self.callback_draw_hline_button)
        self.b_draw_h_line.config(width=8)
        self.b_draw_h_line.grid(row=0, column=2, sticky="NW")
        self.e_hline_pos = My_Float_Entry(self.Area_probe_calc_frame, "hline pos", 0, 0, 3)

        self.e_probe_current = My_Float_Entry(self.Area_probe_calc_frame, "Probe current [mA/cm2]", 1.775, 2, 0)
        self.e_correction_factor = My_Float_Entry(self.Area_probe_calc_frame, "Correction factor", 0.1, 2, 1)
        self.e_probe_area = My_Float_Entry(self.Area_probe_calc_frame, "Probe area [cm^2]", 1, 2, 2)
        self.e_surface_density = My_Float_Entry(self.Area_probe_calc_frame, "RBS density [10^15 atoms/cm2]", 1000, 3, 0)
        self.e_deposition_time = My_Float_Entry(self.Area_probe_calc_frame, "Dep. time [s]", 2700, 3, 1)
        #self.e_deposition_rate = My_Float_Entry(self.Area_probe_calc_frame, "Dep rate [nm/s]", 0.056, 2, 1)
        #self.e_unitcell_volume = My_Float_Entry(self.Area_probe_calc_frame, "Unit cell volume [nm^3]", 0.076317, 3, 0)
        #self.e_atoms_in_unitcell = My_Float_Entry(self.Area_probe_calc_frame, "#Atoms/unit cell", 8, 3, 1)


        ## Langmuir probe calculations
        self.b_fit_langmuir = tk.Button(self.Langmuir_probe_frame, text="Fit to measurement", command=self.callback_fit_langmuir_button)
        self.b_fit_langmuir.config(width=14)
        self.b_fit_langmuir.grid(row=0, column=0, sticky="NW")
        self.b_get_floating_potential = tk.Button(self.Langmuir_probe_frame, text="Calc. Floating", command=self.callback_get_floating_button)
        self.b_get_floating_potential.config(width=11)
        self.b_get_floating_potential.grid(row=0, column=1, sticky="NW")

        self.e_region1_min = My_Float_Entry(self.Langmuir_probe_frame, "Region1 x_Min", -10, 1, 0)
        self.e_region1_max = My_Float_Entry(self.Langmuir_probe_frame, "Region1 x_Max", -5, 1, 1)
        self.e_region2_min = My_Float_Entry(self.Langmuir_probe_frame, "Region2 x_Min", 1, 2, 0)
        self.e_region2_max = My_Float_Entry(self.Langmuir_probe_frame, "Region2 x_Max", 4, 2, 1)

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

        self.positive_currents_data = [] # List of tuples of lists.

        self.fig_plasma = None
        self.ax_plasma = None

        self.fig_langmuir = None
        self.ax_langmuir = None

    def callback_help_button(self):
        Script_Path = Path.cwd()
        rel_path1 = "Supporting_documents\Plasma_probe_calculations.pptx"
        file_path1 = (Script_Path / rel_path1).resolve()
        webbrowser.open_new(file_path1)

    def callback_get_floating_button(self):

        for index, data in enumerate(self.positive_currents_data):
            Voltage = data[0]
            Current = data[1]
            self.print_results("Floating potential [V] = " + str(Voltage[0]))
            self.print_results("Corresponding current [mA]: " + str(Current[0]) + "\n")

    def on_close_langmuir(self, event):
        self.fig_langmuir = None
        self.ax_langmuir = None
    def callback_fit_langmuir_button(self):

        if self.fig_langmuir is None:
            self.fig_langmuir, self.ax_langmuir = plt.subplots(num=Defs.fig_langmuir)
            self.fig_langmuir.canvas.mpl_connect('close_event', self.on_close_langmuir)
        self.ax_langmuir.cla()

        for index, data in enumerate(self.positive_currents_data):
            Voltage = data[0]
            Current = data[1]
            log_current = [math.log10(C) for C in Current]

            region1_V, region1_C = self.get_arrays_in_range(Voltage, log_current, self.e_region1_min.get_value(), self.e_region1_max.get_value())
            region2_V, region2_C = self.get_arrays_in_range(Voltage, log_current, self.e_region2_min.get_value(), self.e_region2_max.get_value())

            coef_R1 = np.polyfit(region1_V, region1_C, 1)
            fit_function_R1 = np.poly1d(coef_R1)

            coef_R2 = np.polyfit(region2_V, region2_C, 1)
            fit_function_R2 = np.poly1d(coef_R2)

            self.ax_langmuir.plot([Voltage[0], Voltage[-1]], [fit_function_R1(Voltage[0]), fit_function_R1(Voltage[-1])], '--k', label="R1 fit")
            self.ax_langmuir.plot([Voltage[0], Voltage[-1]], [fit_function_R2(Voltage[0]), fit_function_R2(Voltage[-1])], '--k', label="R2 fit")

            label = self.data_labels[index].get_value()
            self.ax_langmuir.plot(Voltage, log_current, label=label)
            self.ax_langmuir.set_ylabel("Log current [mA]")

        self.fig_langmuir.suptitle("Fitting to linear regions in log-plot", fontsize=16)
        self.ax_langmuir.set_xlabel("Voltage [V] (Applied bias)")

        self.ax_langmuir.legend()
        self.ax_langmuir.legend().set_draggable(True)
        self.fig_langmuir.show()

    def get_arrays_in_range(self, Voltage, Current, minV, maxV):

        resV = []
        resC = []

        for index, data in enumerate(Voltage):
            if data > minV and data < maxV:
                resV.append(Voltage[index])
                resC.append(Current[index])

        return resV, resC

    # Didn't work too nicely. Quite noicy data...
    def derivative(self, xval, yval):

        yres = []
        xres = []

        for ix in range(len(yval) - 1):
            yres.append((yval[ix+1] - yval[ix]) / (xval[ix+1] - xval[ix]))
            xres.append(xval[ix])

        return xres, yres

    def callback_calc_ion_ratio_button(self):
        e_charge = 1.602176*10**(-19)

        Atom_flux = self.e_surface_density.get_value() * 10**15 / self.e_deposition_time.get_value() # [atoms/(sec*cm2)]
        Ion_flux = self.e_probe_current.get_value() * 0.001 * (1 - self.e_correction_factor.get_value()) / (e_charge * self.e_probe_area.get_value())

        Ion_to_atom_ratio = Ion_flux / Atom_flux

        self.print_results("Atom flux: " + str(Atom_flux))
        self.print_results("Ion flux: " + str(Ion_flux))
        self.print_results("J_ion / J_atom = " + str(Ion_to_atom_ratio) + "\n")

    def callback_draw_vline_button(self):
        xval = self.e_vline_pos.get_value()
        yval_min = -3
        yval_max = 3
        self.ax_plasma.plot([xval, xval], [yval_min, yval_max])
        self.fig_plasma.show()

    def callback_draw_hline_button(self):
        yval = self.e_hline_pos.get_value()
        xval_min = -200
        xval_max = 0
        self.ax_plasma.plot([xval_min, xval_max], [yval, yval])
        self.fig_plasma.show()


    def print_results(self, line):
        self.line_index += 1
        self.result_text.insert("end", "\n")
        self.result_text.insert("end", str(self.line_index)+": ", 'line')
        self.result_text.insert("end", line, 'text')
        self.result_text.tag_config('text', foreground='black')
        self.result_text.tag_config('line', foreground='green')
        self.result_text.yview('end')

    def on_close_plasma(self, event):
        self.fig_plasma = None
        self.ax_plasma = None

    def callback_plot_button(self):

        if self.fig_plasma is None:
            self.fig_plasma, self.ax_plasma = plt.subplots(num=Defs.fig_plasma)
            self.fig_plasma.canvas.mpl_connect('close_event', self.on_close_plasma)
        self.ax_plasma.cla()


        if self.plot_selection_index == 0:  # Linear
            for index, data in enumerate(self.file_data):
                Voltage = data.get_col1()
                Current = data.get_col2()
                label = self.data_labels[index].get_value()
                self.ax_plasma.plot(Voltage, Current, label=label)
                self.ax_plasma.set_ylabel("Current [mA]")

        elif self.plot_selection_index == 1: # Log
            for index, data in enumerate(self.positive_currents_data):
                Voltage = data[0]
                Current = data[1]
                #print(data)
                #print("Voltage: ", Voltage)
                #print("Current: ", Current)

                label = self.data_labels[index].get_value()
                self.ax_plasma.plot(Voltage, [math.log10(C) for C in Current], label=label)
                #self.ax_langmuir.set_yscale('log')
                self.ax_plasma.set_ylabel("Log current [mA]")


        self.fig_plasma.suptitle("Plasma I-V curve", fontsize=16)
        self.ax_plasma.set_xlabel("Voltage [V] (Applied bias)")

        self.ax_plasma.legend()
        self.ax_plasma.legend().set_draggable(True)
        self.fig_plasma.show()
        pass


    def callback_import_all_button(self):
        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns_plasma_probe(0)
            self.file_data.append(data_in_file)
            self.add_version_for_log(data_in_file)

            new_entry = My_Label_Entry(self.label_entry_frame, data_in_file.file_name, self.no_files_index, 0)
            new_entry.set_label_bg("seagreen1")
            new_entry.set_entry_value(data_in_file.file_name)
            self.data_labels.append(new_entry)


    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns_plasma_probe(0)
        self.file_data.append(data)
        self.add_version_for_log(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def add_version_for_log(self, data):
        Res_V = []
        Res_C = []
        Voltage = data.get_col1()
        Current = data.get_col2()

        for ix, val in enumerate(Current):
            if val >= 0 :
                Res_C.append(Current[ix])
                Res_V.append(Voltage[ix])

        self.positive_currents_data.append((Res_V, Res_C))


    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels:
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []
        self.positive_currents_data[:] = []

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