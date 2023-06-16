import os
import tkinter as tk

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
from Util.My_Path_Button import My_Path_Button
from Util.Color_Scheme_Selector import Color_Scheme_Selector
import Synchrotron_diffraction.Synchrotron_popup as popup

import pyFAI as pyFAI
import pathlib as Path
import fabio as fabio

import tkscrolledframe as SF
import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams
import matplotlib.cm as cm
import numpy as np
import Util.Definitions as Defs
import json as json
import math as math


Description = """This script is an imaging script for viewing 2D
images, especially for synchrotron data

First open the files you want to use and import 

"""

class Plugin_2D_Image:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler # to get data from

        self.active = False
        self.savable_script = False

        # Private frames
        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)  # Master within this scope

        self.sframe = SF.ScrolledFrame(self.my_frame, width=400, height=90)
        self.sframe.grid(row=15, column=0, columnspan=3)
        self.sframe.config(bg=Defs.c_frame_color)
        self.sframe.bind_arrow_keys(self.my_frame)
        self.sframe.bind_scroll_wheel(self.my_frame)
        self.label_entry_frame = self.sframe.display_widget(tk.Frame)
        self.label_entry_frame.config(bg=Defs.c_frame_color)

        self.master_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.master_button_frame.grid(row=3, column=0, columnspan=3)
        self.select_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.select_button_frame.grid(row=4, column=0, columnspan=3)

        self.entry_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.entry_frame.grid(row=5, column=0, columnspan=3)

        self.help_stuff_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.help_stuff_frame.grid(row=6, column=0, columnspan=3)


        self.integrate_2d_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.integrate_2d_frame.grid(row=11, column=0, columnspan=3)
        self.integrate_1d_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.integrate_1d_frame.grid(row=12, column=0, columnspan=3)
        self.integrate_multiple_1d_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.integrate_multiple_1d_frame.grid(row=13, column=0, columnspan=3)

        # Master label
        self.label = tk.Label(self.my_frame, text="Synchrotron data analysis", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Master description text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        self.b_import = tk.Button(self.master_button_frame, text="Import", command=self.callback_import_image_button)
        self.b_import.config(width=8)
        self.b_import.grid(row=0, column=0, sticky="NW")
        self.b_load_img = tk.Button(self.master_button_frame, text="Load img", command=self.callback_load_image_button)
        self.b_load_img.config(width=8)
        self.b_load_img.grid(row=0, column=1, sticky="NW")
        self.b_plot = tk.Button(self.master_button_frame, text="Plot", command=self.callback_plot_button)
        self.b_plot.config(width=8)
        self.b_plot.grid(row=0, column=2, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files", command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=3, sticky="NW")
        self.b_settings_popup = tk.Button(self.master_button_frame, text="Settings", command=self.callback_settings_popup)
        self.b_settings_popup.config(width=8)
        self.b_settings_popup.grid(row=0, column=4, sticky="NW")

        self.selection_index = 1
        self.b_linear = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=3, column=0, sticky="NW")
        self.b_log = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=3, column=1, sticky="NW")
        self.b_test_function = tk.Button(self.select_button_frame, text="Test fkn", command=self.callback_test_function)
        self.b_test_function.grid(row=3, column=2, sticky="NW")

        ## Entries
        self.Entry_min_clim = My_Float_Entry(self.entry_frame, "Min clim", 0, 2, 0)
        self.Entry_min_clim.set_entry_width(5)
        self.Entry_max_clim = My_Float_Entry(self.entry_frame, "Max clim", 100000, 2, 1)
        self.Entry_max_clim.set_entry_width(10)

        ## Color scheme
        self.color_scheme = Color_Scheme_Selector(self.entry_frame, 'jet', 2, 2)

        ## Integration Cake plotting
        self.b_cake_plot_button = tk.Button(self.entry_frame, text="Plot cake", command=self.callback_cake_plot_button)
        self.b_cake_plot_button.grid(row=3, column=0, sticky="NW")

        self.e_cake_centre_x = My_Float_Entry(self.entry_frame, "Centre X [px]", 1015.781, 3, 1)
        self.e_cake_centre_y = My_Float_Entry(self.entry_frame, "Centre Y [px]", 1006.800, 3, 2)
        self.e_cake_radius = My_Float_Entry(self.entry_frame, "Radius [px]", 1000, 4, 1)
        self.e_cake_total_angle = My_Float_Entry(self.entry_frame, "Angle [\u00b0]", 10, 4, 2)

        ## 1D integration: Just one.
        self.b_integrate_1d = tk.Button(self.integrate_1d_frame, text="1D integr.", command=self.callback_1D_integration)
        self.b_integrate_1d.grid(row=0, column=0, sticky="NW")
        self.selection_integrate_axis = 0 # 0 = tth, 1 = d_hkl
        self.b_integrate_1d_tth = tk.Button(self.integrate_1d_frame, text="2\u03B8 [\u00B0]", command=self.callback_1D_tth)
        self.b_integrate_1d_tth.grid(row=1, column=0, sticky="NW")
        self.b_integrate_1d_d_hkl = tk.Button(self.integrate_1d_frame, text="d\u2095\u2096\u2097", command=self.callback_1D_d_hkl)
        self.b_integrate_1d_d_hkl.grid(row=1, column=1, sticky="NW")
        self.callback_1D_tth()
        self.e_n_pts_1d = My_Float_Entry(self.integrate_1d_frame, "# Pts", 2000, 0, 1)
        self.e_psi_start = My_Float_Entry(self.integrate_1d_frame, "\u03C8 min [\u00B0]", 80, 0, 2)
        self.e_psi_end = My_Float_Entry(self.integrate_1d_frame, "\u03C8 max [\u00B0]", 100, 0, 3)
        self.e_tth_int1D_max = My_Float_Entry(self.integrate_1d_frame, "2\u03B8 max [\u00B0]", 6, 1, 3)
        self.e_tth_int1D_min = My_Float_Entry(self.integrate_1d_frame, "2\u03B8 min [\u00B0]", 2, 1, 2)

        ## 1D integration: Multiple + save each in file.
        label_text = "Integrates in steps and saves the data in files.\nSave folder is specified in Settings."
        self.l_multiple_integration = tk.Label(self.integrate_multiple_1d_frame, text=label_text, bg=Defs.c_script_name)
        self.l_multiple_integration.grid(row=0, column=0, columnspan=5)
        self.b_multiple_integration_1d = tk.Button(self.integrate_multiple_1d_frame, text="Integ multiple", command=self.callback_multiple_1D_integration)
        self.b_multiple_integration_1d.grid(row=1, column=0, sticky="NW")
        self.e_multiple_file_name = My_Label_Entry(self.integrate_multiple_1d_frame, "File Name", 1, 1, 5)
        self.e_multiple_file_name.set_entry_value("sample")
        self.e_multiple_n_pts_1d = My_Float_Entry(self.integrate_multiple_1d_frame, "# Pts", 1000, 2, 1)
        self.e_multiple_psi_start = My_Float_Entry(self.integrate_multiple_1d_frame, "\u03C8 min [\u00B0]", 0, 2, 2)
        self.e_multiple_psi_end = My_Float_Entry(self.integrate_multiple_1d_frame, "\u03C8 max [\u00B0]", 180, 2, 3)
        self.e_multiple_psi_step = My_Float_Entry(self.integrate_multiple_1d_frame, "\u03C8 step [\u00B0]", 10, 2, 4)
        self.e_multiple_tth_int1D_max = My_Float_Entry(self.integrate_multiple_1d_frame, "2\u03B8 max [\u00B0]", 7, 3, 3)
        self.e_multiple_tth_int1D_min = My_Float_Entry(self.integrate_multiple_1d_frame, "2\u03B8 min [\u00B0]", 2, 3, 2)

        ## 2D integration
        self.b_Azi_integr = tk.Button(self.integrate_2d_frame, text="Conv. \u03C6 vs 2\u03B8 ", command=self.callback_azim_integration)
        self.b_Azi_integr.grid(row=0, column=0, sticky="NW")
        self.e_npt_2d_rad = My_Float_Entry(self.integrate_2d_frame, "#pt 2\u03B8", 500, 0, 1)
        self.e_npt_2d_azim = My_Float_Entry(self.integrate_2d_frame, "#pt \u03C8", 500, 0, 2)
        self.e_2th_2d_max = My_Float_Entry(self.integrate_2d_frame, "2\u03B8 max", 6, 0, 4)
        self.e_2th_2d_min = My_Float_Entry(self.integrate_2d_frame, "2\u03B8 min", 2, 0, 3)

        ## Help stuff

        ## Objects to operate on.
        self.o_azimutal_integration = None # Is the settings for how integrating shall be done. Based on PONI file...

        # The imported image.
        self.o_IMG = None
        # The output after 1D integration is done.
        self.o_result_1d_integr = None
        # The output after 2D integration is done.
        self.o_result_2d_integr = None



        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

        self.fig = None
        self.axis = None
        self.fig_1d_integr = None
        self.axis_1d_integr = None
        self.fig_multi_1d = None
        self.axis_multi_1d = None
        self.fig_2d_integr = None
        self.axis_2d_integr = None
        self.fig_polar_coord = None
        self.axis_polar_coord = None


        # Internal data
        self.Path_to_Cal_file = ""
        self.Path_to_PONI_file = ""
        self.Path_to_save_folder = ""
        self.Beam_Energy = 73.8 # in keV

        # Setting up the class.
        self.callback_linear_button() # To setup correctly
        self.parse_json_settings() # Parse last locations entered.


    def on_close_synchr_image(self, event):
        print("closed window")
        self.fig = None
        self.axis = None

    def callback_plot_button(self):
        if self.fig is None:
            self.fig, self.axis = plt.subplots(num=Defs.fig_nr_synchr_image)
            self.fig.canvas.mpl_connect('close_event', self.on_close_synchr_image)

        self.axis.cla()
        Fixed_IMG = self.o_IMG
        # To make set_clim work, must have an L-value image from imshow...
        image = self.axis.imshow(Fixed_IMG, cmap=self.color_scheme.get_color(), origin='lower')
        image.set_clim(self.Entry_min_clim.get_value(), self.Entry_max_clim.get_value())

        self.axis.set_xlabel("Pixels")
        self.axis.set_ylabel("Pixels")
        self.fig.suptitle("Raw image", fontsize=16)
        self.fig.show()

    def get_wavelength(self):
        # Energy should be in keV !!!
        # Return the wavelenght in m
        # -----------------------------------
        energy = self.Beam_Energy

        # Plank Constant
        h = 6.62607004e-34  # m2 . kg / s
        # light celerity
        c = 299792458  # m / s
        # Joule -> eV
        eV = 6.242e+18  # eV / J

        # Conversion Energy -> wavelenght
        wavelenght = ((h * c) / (energy * 1e3 / eV))  # m

        return wavelenght

    def on_close_multi_integr_1D_image(self, event):
        print("closed window")
        self.fig_multi_1d = None
        self.axis_multi_1d = None

    def callback_multiple_1D_integration(self):
        if self.fig_multi_1d is None:
            self.fig_multi_1d, self.axis_multi_1d = plt.subplots(num=Defs.fig_multi_1d_sycnhr_integr)
            self.fig_multi_1d.canvas.mpl_connect('close_event', self.on_close_multi_integr_1D_image)
        self.axis_multi_1d.cla()

        two_theta_max = self.e_multiple_tth_int1D_max.get_value()
        two_theta_min = self.e_multiple_tth_int1D_min.get_value()
        theta_range = [two_theta_min, two_theta_max]

        # todo: calculate the number of points needed. (user input today...)

        psi_max = self.e_multiple_psi_end.get_value()
        psi_min = self.e_multiple_psi_start.get_value()
        psi_step = self.e_multiple_psi_step.get_value()
        No_of_integrations = int((psi_max-psi_min) / psi_step)

        cmap = cm.get_cmap('jet', No_of_integrations)

        for step in range(No_of_integrations):

            psi_range = [psi_min + step * psi_step, psi_min + (step + 1) * psi_step]

            file_name = self.e_multiple_file_name.get_value() + str(psi_range[0]) + "_to_" + str(psi_range[1]) + ".dat"
            complete_path = self.Path_to_save_folder + "/" + file_name

            res = self.o_azimutal_integration.integrate1d(self.o_IMG, npt=self.e_multiple_n_pts_1d.get_value(),
                                                          unit="2th_deg", azimuth_range=psi_range,
                                                          radial_range=theta_range,
                                                          filename=complete_path)
            I = res.intensity
            Tth = res.radial
            # d_space = self.get_wavelength() * 1e10 / (2 * np.sin(np.radians(Tth/2)))

            data_label = "\u03C6 \u2208 " + str(psi_range[0]) + ", " + str(psi_range[1]) + " [\u00B0]"
            self.axis_multi_1d.plot(Tth, I, marker="o", linestyle="--", alpha=0.4, markersize=4,
                                    color=cmap(step), label=data_label)


        self.axis_multi_1d.set_xlabel("2\u03B8 [\u00B0]")
        self.axis_multi_1d.set_ylabel("Intensity (arb. unit)")
        self.axis_multi_1d.legend().set_draggable(True)
        self.fig_multi_1d.suptitle(self.e_multiple_file_name.get_value())
        self.fig_multi_1d.show()


    def on_close_integr_1D_image(self, event):
        print("closed window")
        self.fig_1d_integr = None
        self.axis_1d_integr = None

    def callback_1D_integration(self):

        two_theta_max = self.e_tth_int1D_max.get_value()
        two_theta_min = self.e_tth_int1D_min.get_value()
        azim_range = [self.e_psi_start.get_value(), self.e_psi_end.get_value()]
        rad_range = [two_theta_min, two_theta_max]

        self.o_result_1d_integr = self.o_azimutal_integration.integrate1d(self.o_IMG, npt=self.e_n_pts_1d.get_value(),
                                                                          unit="2th_deg", azimuth_range=azim_range,
                                                                          radial_range=rad_range)

        I = self.o_result_1d_integr.intensity
        Tth = self.o_result_1d_integr.radial
        d_space = self.get_wavelength() * 1e10 / (2 * np.sin(np.radians(Tth/2)))

        if self.fig_1d_integr is None:
            self.fig_1d_integr, self.axis_1d_integr = plt.subplots(num=Defs.fig_1d_synchr_integr)
            self.fig_1d_integr.canvas.mpl_connect('close_event', self.on_close_integr_1D_image)
        self.axis_1d_integr.cla()

        if self.selection_integrate_axis == 0: # tth
            self.axis_1d_integr.plot(Tth, I, marker="o", linestyle="--", alpha=0.4, markersize=4)
            self.axis_1d_integr.set_xlabel(r"$2\mathrm{\theta \ (^o)} $ ")

        elif self.selection_integrate_axis == 1:  # d_hkl
            self.axis_1d_integr.plot(d_space, I, marker="o", linestyle="--", alpha=0.4, markersize=4)
            self.axis_1d_integr.set_xlabel("d\u2095\u2096\u2097 [Å]")


        if self.selection_index == 0:  # Linear
            self.axis_1d_integr.set_yscale('linear')
            self.axis_1d_integr.set_ylabel("Intensity (arbitraty unit)")

        elif self.selection_index == 1: # Log
            self.axis_1d_integr.set_yscale('log')
            self.axis_1d_integr.set_ylabel("Log intensity (arbitraty unit)")



        title_first = "Integrated "
        title_pts = str(self.e_n_pts_1d.get_value()) + " points, "
        title_range = "\u03C8 = [" + str(self.e_psi_start.get_value()) + "\u00B0, " + str(self.e_psi_end.get_value()) + "\u00B0] "
        self.fig_1d_integr.suptitle(title_first + title_pts + title_range)

        self.fig_1d_integr.show()

    def on_close_synchr_2D_image(self, event):
        print("closed window")
        self.fig_2d_integr = None
        self.axis_2d_integr = None

    def callback_azim_integration(self):

        rad_range = [self.e_2th_2d_min.get_value(), self.e_2th_2d_max.get_value()]
        self.o_result_2d_integr = self.o_azimutal_integration.integrate2d(self.o_IMG,
                                                                          npt_rad=int(self.e_npt_2d_rad.get_value()),
                                                                          npt_azim=int(self.e_npt_2d_azim.get_value()),
                                                                          unit="2th_deg",
                                                                          azimuth_range=[-180, 180],
                                                                          radial_range=rad_range)

        I, tth, chi = self.o_result_2d_integr

        rcParams["image.cmap"] = self.color_scheme.get_color()
        if self.fig_2d_integr is None:
            self.fig_2d_integr, self.axis_2d_integr = plt.subplots(num=Defs.fig_2d_synchr_integr)
            self.fig_2d_integr.canvas.mpl_connect('close_event', self.on_close_synchr_2D_image)
        self.axis_2d_integr.cla()

        image_2D = self.axis_2d_integr.imshow(I, origin="lower", extent=[tth.min(), tth.max(), chi.min(), chi.max()],
                                    aspect="auto", vmin=self.Entry_min_clim.get_value(),
                                              vmax=self.Entry_max_clim.get_value())
        self.axis_2d_integr.set_xlabel(r"$2\mathrm{\theta \ (^o)} $ ")
        self.axis_2d_integr.set_ylabel("Azimuthal angle $\mathrm{\Phi \ (^o)} $ ")

        self.fig_2d_integr.show()

    def callback_import_image_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

        self.e_multiple_file_name.set_entry_value(data.file_name)

    def callback_load_image_button(self):
        File_path = self.file_data[0].get_path()
        IMG_Raw = fabio.open(File_path)
        self.o_IMG = IMG_Raw.data  # The return value "IMG" is a numpy array...

        self.o_azimutal_integration = pyFAI.load(self.Path_to_PONI_file)
        print("Geometry loaded:")
        print(self.o_azimutal_integration)

    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels :
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []

    def callback_settings_popup(self):
        popup.Synchrotron_popup(self)

    def callback_1D_tth(self):
        self.selection_integrate_axis = 0
        self.unmark_axis_selection()
        self.b_integrate_1d_tth.config(bg=Defs.c_button_active)

    def callback_1D_d_hkl(self):
        self.selection_integrate_axis = 1
        self.unmark_axis_selection()
        self.b_integrate_1d_d_hkl.config(bg=Defs.c_button_active)

    def unmark_axis_selection(self):
        self.b_integrate_1d_tth.config(bg=Defs.c_button_inactive)
        self.b_integrate_1d_d_hkl.config(bg=Defs.c_button_inactive)

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

    def callback_test_function(self):
        print("Test function")

    def callback_cake_plot_button(self):
        x_0 = self.e_cake_centre_x.get_value()
        y_0 = self.e_cake_centre_y.get_value()
        radius = self.e_cake_radius.get_value()
        angle = self.e_cake_total_angle.get_value()

        x_1 = x_0 + radius * math.sin(math.radians(angle))
        y_1 = y_0 + radius * math.cos(math.radians(angle))

        x_2 = x_0 - radius * math.sin(math.radians(angle))
        y_2 = y_0 + radius * math.cos(math.radians(angle))

        x_3 = x_0
        y_3 = y_0 + radius

        self.axis.plot([x_0, x_1], [y_0, y_1], ls='dotted', linewidth=2, color='red')
        self.axis.plot([x_0, x_2], [y_0, y_2], ls='dotted', linewidth=2, color='red')
        self.axis.plot([x_0, x_3], [y_0, y_3], ls='dotted', linewidth=2, color='red')
        self.fig.show()

    def parse_json_settings(self):

        with open("PDF_user_config/json_file_paths.txt", "r") as infile:
            data = json.load(infile)
            paths = data['paths']
            # print(paths[0]['PONI'])
            self.Path_to_Cal_file = paths[0]['Calibration']
            self.Path_to_PONI_file = paths[0]['PONI']
            self.Path_to_save_folder = paths[0]['save_location']


    def save_data_to_json_file(self):

        Aggregated_Data = {}
        Aggregated_Data['paths'] = []

        Aggregated_Data['paths'].append(
            {
                'Calibration': self.Path_to_Cal_file,
                'PONI': self.Path_to_PONI_file,
                'save_location': self.Path_to_save_folder
            }
        )
        with open("PDF_user_config/json_file_paths.txt", "w") as outfile:
            json.dump(Aggregated_Data, outfile, indent=4)



    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()

    def __del__(self):
        self.save_data_to_json_file()
