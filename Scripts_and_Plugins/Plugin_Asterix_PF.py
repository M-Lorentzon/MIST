import math
import re
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import tkscrolledframe as SF

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
import Util.Definitions as Defs
from Text_Plotter import Text_Plotter
import Util.My_SF_Selection_Entry_Container as SF_cont

from Util.List_Of_Strings_Container import List_Of_Strings_Container

Description = """This script treats pole figure XRD data

It only works with pole figure files from Asterix 

First open the file you want to use and import 
it into the script environment. Then fix the 
chi and phi steps manually. 

'Calculate' extracts important data into  
columns and a new file can be saved. 'Plot' 
creates 2D and 3D pole figures that can be saved. 

Use buttons and entries to modify the figures

"""

class Plugin_Asterix_PF:

    def __init__(self, Script_frame, file_handler, text_plotter):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler # to get data from
        self.o_text_plotter = text_plotter # to be able to plot the data

        self.active = False
        self.savable_script = True

        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)

        self.sframe = SF.ScrolledFrame(self.my_frame, width=400, height=200)
        self.sframe.grid(row=10, column=0, columnspan=3)
        self.sframe.config(bg=Defs.c_frame_color)
        self.sframe.bind_arrow_keys(self.my_frame)
        self.sframe.bind_scroll_wheel(self.my_frame)
        self.label_entry_frame = self.sframe.display_widget(tk.Frame)
        self.label_entry_frame.config(bg=Defs.c_frame_color)

        self.master_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.master_button_frame.grid(row=3, column=0)
        self.entry_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.entry_frame.grid(row=4, column=0)

        self.plot_selection_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.plot_selection_frame.grid(row=5, column=0)
        self.plot_2D_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.plot_2D_frame.grid(row=6, column=0)
        self.plot_3D_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.plot_3D_frame.grid(row=7, column=0)

        # Master Label
        self.label = tk.Label(self.my_frame, text="Pole figure script settings", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Description Text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Entries
        self.Entry_Chi_Min = My_Float_Entry(self.entry_frame, "Chi Min", 0, 2, 0)
        self.Entry_Chi_Max = My_Float_Entry(self.entry_frame, "Chi Max", 0, 2, 1)
        self.Entry_Chi_step = My_Float_Entry(self.entry_frame, "Chi step", 0, 2, 2)

        self.Entry_Phi_Min = My_Float_Entry(self.entry_frame, "Phi Min", 0, 3, 0)
        self.Entry_Phi_Max = My_Float_Entry(self.entry_frame, "Phi Max", 0, 3, 1)
        self.Entry_Phi_step = My_Float_Entry(self.entry_frame, "Phi step", 0, 3, 2)

        self.Entry_Wavelenght = My_Float_Entry(self.entry_frame, "Wavelength", 0, 4, 0)
        self.Entry_Two_Theta = My_Float_Entry(self.entry_frame, "2Theta", 0, 4, 1)
        self.Entry_No_Data_Pts = My_Float_Entry(self.entry_frame, "Data Pts", 0, 4, 2)

        self.Entry_phi_offset = My_Float_Entry(self.entry_frame, "Phi offset", 0, 5, 1)


        # Master Buttons
        self.b_import = tk.Button(self.master_button_frame, text="Import", command=self.callback_import_button)
        self.b_import.config(width=8)
        self.b_import.grid(row=0, column=0, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files", command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=2, sticky="NW")
        self.b_plot = tk.Button(self.master_button_frame, text="Plot", command=self.callback_plot_button)
        self.b_plot.config(width=8)
        self.b_plot.grid(row=0, column=4, sticky="NW")

        # Selection buttons
        self.plot_selection_index = 1
        self.b_linear = tk.Button(self.plot_selection_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=0, column=0, sticky="NW")
        self.b_linear.config(width=8)
        self.b_log = tk.Button(self.plot_selection_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=0, column=1, sticky="NW")
        self.b_log.config(width=8)
        self.b_sqrt = tk.Button(self.plot_selection_frame, text="SQRT", command=self.callback_sqrt_button)
        self.b_sqrt.grid(row=0, column=2, sticky="NW")
        self.b_sqrt.config(width=8)
        self.callback_linear_button() # Start with Linear as default!

        # Plotting 2D buttons etc.
        self.Entry_2D_plot_label = My_Label_Entry(self.plot_2D_frame, "Plot title", 2, 0, 4)
        self.Entry_2D_plot_label.set_entry_value("Pole figure 2D")

        self.selection_axis_mode = 1 # 0=off, 1=on
        self.b_axis_on = tk.Button(self.plot_2D_frame, text="Axis On", command=self.callback_axis_on_2D_button)
        self.b_axis_on.config(width=8)
        self.b_axis_on.grid(row=5, column=0, sticky="NW")
        self.b_axis_off = tk.Button(self.plot_2D_frame, text="Axis Off", command=self.callback_axis_off_2D_button)
        self.b_axis_off.config(width=8)
        self.b_axis_off.grid(row=5, column=1, sticky="NW")
        self.selection_colorbar_enable = 1 # 0=off, 1=on
        self.b_color_selection = tk.Button(self.plot_2D_frame, text="Color bar", command=self.callback_colorbar_button)
        self.b_color_selection.config(width=8)
        self.b_color_selection.grid(row=5, column=2, sticky="NW")
        self.callback_colorbar_button()

        self.b_update_axis = tk.Button(self.plot_2D_frame, text="Update", command=self.callback_update_axis_2D_button)
        self.b_update_axis.config(width=8)
        self.b_update_axis.grid(row=6, column=0, sticky="NW")
        self.Entry_theta_spacing = My_Float_Entry(self.plot_2D_frame, "Theta axis", 45, 6, 1)
        self.Entry_Chi_spacing = My_Float_Entry(self.plot_2D_frame, "Chi axis", 20, 7, 1)

        self.b_test = tk.Button(self.plot_2D_frame, text="*Testing*", command=self.callback_test_2D_button)
        self.b_test.config(width=8)
        self.b_test.grid(row=10, column=0, sticky="NW")

        # Plotting 3D buttons etc.
        self.Entry_3D_plot_label = My_Label_Entry(self.plot_3D_frame, "Plot title", 2, 0, 4)
        self.Entry_3D_plot_label.set_entry_value("Pole figure 3D")


        # File data imported in form of container class
        self.no_files_index = 0
        self.phi_list = []
        self.chi_list = []
        self.file_data = []
        self.label_container = SF_cont.My_SF_Selection_Entry_Container(self.my_frame, 400, 200, 10, 0)

        # Results stored from concatenating and calculating all imported files.
        self.results = List_Of_Strings_Container()

        # Plotting objects and settings
        self.fig_2D = None
        self.ax_2D = None

        self.fig_3D = None
        self.ax_3D = None

    def callback_plot_button(self):
        self.plot_3D()
        self.plot_2D()
        plt.show()

    def on_close_3D_fig(self, event):
        print("closed window")
        self.fig_3D = None
        self.ax_3D = None

    def plot_3D(self):

        if self.fig_3D is None:
            self.fig_3D = plt.figure(Defs.fig_asterix_PF_3D)
            self.ax_3D = self.fig_3D.add_subplot(projection='3d')
            self.fig_3D.suptitle("Pole figure 3D: ", fontsize=16)
            self.fig_3D.canvas.mpl_connect('close_event', self.on_close_3D_fig)

        self.ax_3D.cla()

        Phi_, Chi_ = np.meshgrid(np.radians(self.phi_list), self.chi_list)
        Z = np.array(self.get_z_values())

        #print("Thetas: ", len(Thetas), "Azimuths: ", len(Azimuths), "Z: ", len(Z))


        Thetas_2D_array, Azimuths_2D_array = np.meshgrid(np.radians(self.phi_list), self.chi_list)

        X = Azimuths_2D_array * np.cos(Thetas_2D_array)
        Y = Azimuths_2D_array * np.sin(Thetas_2D_array)

        self.fig_3D.suptitle(self.Entry_3D_plot_label.get_value(), fontsize=16)

        self.ax_3D.plot_surface(X, Y, Z, cmap='jet', alpha=0.75)
        #self.ax_3D.set_axis_off()


    def callback_update_axis_2D_button(self):
        Thetas = range(0, 360, int(self.Entry_theta_spacing.get_value()))
        self.ax_2D.set_xticks(np.radians(Thetas))

        Small_Chi = self.chi_list[0]
        Large_Chi = self.chi_list[-1]
        Chis = range(int(Small_Chi), int(Large_Chi), int(self.Entry_Chi_spacing.get_value()))
        self.ax_2D.set_yticks(Chis)
        plt.show()

    def callback_test_2D_button(self):
        print("Test button")  # Keep this line

    def callback_axis_on_2D_button(self):
        self.selection_axis_mode = 1
        self.b_axis_on.config(bg=Defs.c_button_active)
        self.b_axis_off.config(bg=Defs.c_button_inactive)
        self.ax_2D.set_axis_on()
        plt.show()

    def callback_axis_off_2D_button(self):
        self.selection_axis_mode = 0
        self.b_axis_on.config(bg=Defs.c_button_inactive)
        self.b_axis_off.config(bg=Defs.c_button_active)
        self.ax_2D.set_axis_off()
        plt.show()

    def callback_colorbar_button(self):
        if self.selection_colorbar_enable == 1:
            self.selection_colorbar_enable = 0
            self.b_color_selection.config(bg=Defs.c_button_inactive)

        else:
            self.selection_colorbar_enable = 1
            self.b_color_selection.config(bg=Defs.c_button_active)

    def on_close_2D_fig(self, event):
        print("closed window")
        self.fig_2D = None
        self.ax_2D = None

    def plot_2D(self):
        
        if self.fig_2D is None:
            self.fig_2D, self.ax_2D = plt.subplots(num=Defs.fig_asterix_PF_2D, subplot_kw={'projection': 'polar'})
            self.fig_2D.suptitle("Pole figure 2D: ", fontsize=16)
            self.fig_2D.canvas.mpl_connect('close_event', self.on_close_2D_fig)

        self.ax_2D.cla()
        # ____________
        #print("Len Chis: ", len(self.chi_list))
        #print("Len Phis: ", len(self.phi_list))
        #print("Len values: ", len(self.file_data))

        phi_list_offset = [phi + self.Entry_phi_offset.get_value() for phi in self.phi_list]

        # Create 2D-arrays of polar coordinates
        Phi_, Chi_ = np.meshgrid(np.radians(phi_list_offset), self.chi_list)
        Values = np.array(self.get_z_values())


        #print("Values shape: ", Values.shape)
        #print("Phi_ shape: ", Phi_.shape)
        #print("Chi_ shape", Chi_.shape)

        cax = self.ax_2D.contourf(Phi_, Chi_, Values, 75, cmap='jet')
        self.ax_2D.set_theta_zero_location("N")
        self.ax_2D.set_theta_direction(-1)
        if self.selection_colorbar_enable == 1:
            cb = self.fig_2D.colorbar(cax, pad=0.15)
            cb.set_label(self.get_2d_counts_label())

        self.fig_2D.suptitle(self.Entry_2D_plot_label.get_value(), fontsize=16)

        self.callback_update_axis_2D_button()

    def get_z_values(self):
        temp_values = []

        for sublist in self.file_data:
            Temp_list = []
            if self.plot_selection_index == 0:  # lin
                Temp_list = sublist
            elif self.plot_selection_index == 1:  # log
                for element in sublist:
                    Temp_list.append(math.log(element+1))
            elif self.plot_selection_index == 2:
                for element in sublist:
                    Temp_list.append(math.sqrt(element))
            #print(Temp_list)
            temp_values.append(Temp_list)

        return temp_values

    def get_2d_counts_label(self):
        ret_val = ""
        if self.plot_selection_index == 0: #lin
            ret_val = "Counts"
        elif self.plot_selection_index == 1: #log
            ret_val = "Log(Counts)"
        elif self.plot_selection_index == 2:  # sqrt
            ret_val = "Sqrt(Counts)"
        return ret_val

    def callback_import_button(self):
        # Import raw data from data_container since this is an atypical data storage.
        # I.e. treat it differently from other scripts...

        self.no_files_index += 1
        data_container = self.o_file_handler.get_current_data()
        Raw_Data = data_container.list_of_lines

        min_data_index = 21
        Chi_Min = float(re.split(',', Raw_Data[16])[1])
        Chi_Max = float(re.split(',', Raw_Data[16])[2])
        Chi_Step = float(re.split(',', Raw_Data[16])[3])
        Phi_Min = float(re.split(',', Raw_Data[17])[1])
        Phi_Max = float(re.split(',', Raw_Data[17])[2])
        Phi_Step = float(re.split(',', Raw_Data[17])[3])
        Wavelength = float(re.split(',', Raw_Data[7])[1])
        Two_Theta = float(re.split(',', Raw_Data[13])[1])
        No_Data_Pts = int(re.split(',', Raw_Data[19])[1])
        filename = str(re.split(',', Raw_Data[0])[1])


        self.Entry_Chi_Min.set_entry_value(Chi_Min)
        self.Entry_Chi_Max.set_entry_value(Chi_Max)
        self.Entry_Chi_step.set_entry_value(Chi_Step)
        self.Entry_Phi_Min.set_entry_value(Phi_Min)
        self.Entry_Phi_Max.set_entry_value(Phi_Max)
        self.Entry_Phi_step.set_entry_value(Phi_Step)
        self.Entry_Wavelenght.set_entry_value(Wavelength)
        self.Entry_Two_Theta.set_entry_value(Two_Theta)
        self.Entry_No_Data_Pts.set_entry_value(No_Data_Pts)
        self.Entry_3D_plot_label.set_entry_value(filename)
        self.Entry_2D_plot_label.set_entry_value(filename)

        No_Chis = int(Chi_Max / Chi_Step) + 1
        No_Phis_per_chi = int(Phi_Max / Phi_Step)

        Phis = [i * Phi_Step for i in range(No_Phis_per_chi)]
        Chis = [i * Chi_Step for i in range(No_Chis)]
        Values = []

        for ix in range(No_Chis):
            start_index = ix * No_Phis_per_chi + min_data_index
            end_index = start_index + No_Phis_per_chi

            cts = Raw_Data[start_index : end_index]
            Values.append(cts)

        self.chi_list = Chis
        self.phi_list = Phis
        temp = [[int(s) for s in sublist] for sublist in Values]
        self.file_data = temp

        ## Show the name of the file imported.
        self.label_container.add_float_entry(data_container.file_name, Chi_Step)

        #print("Phis: ", Phis)
        #print("Chis: ", Chis)
        #print("Values: ", Values)


    def callback_clear_files_button(self):
        self.file_data.clear()
        self.label_container.remove_all_entries()
        self.no_files_index = 0


    def get_results(self):
        return self.results.get_list()

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()

    def callback_linear_button(self):
        self.plot_selection_index = 0
        self.unmark_select_buttons()
        self.b_linear.config(bg=Defs.c_button_active)

    def callback_log_button(self):
        self.plot_selection_index = 1
        self.unmark_select_buttons()
        self.b_log.config(bg=Defs.c_button_active)

    def callback_sqrt_button(self):
        self.plot_selection_index = 2
        self.unmark_select_buttons()
        self.b_sqrt.config(bg=Defs.c_button_active)

    def unmark_select_buttons(self):
        self.b_linear.config(bg=Defs.c_button_inactive)
        self.b_log.config(bg=Defs.c_button_inactive)
        self.b_sqrt.config(bg=Defs.c_button_inactive)
