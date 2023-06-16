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

It only works with '.xy'-files and only for 
complete pole figures, i.e. phi from 0 - 360. 
(E.g. phi = {2.5, 7.5, ..., 355 357.5} works) 

First open the files you want to use and import 
them into the script environment either one by one
or all opened files at once. If the files are
sorted, the Chi-value has already been filled in
as specified in the 'Chi step' input. 

'Calculate' extracts important data into  
columns and a new file can be saved. 'Plot' 
creates 2D and 3D pole figures that can be saved. 

Use buttons and entries to modify the figures

"""

class Plugin_Pole_fig:

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
        self.Entry_Chi = My_Float_Entry(self.entry_frame, "Chi step", 5, 2, 0)

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
        self.b_calculate = tk.Button(self.master_button_frame, text="Calculate", command=self.callback_calculate_button)
        self.b_calculate.config(width=8)
        self.b_calculate.grid(row=0, column=3, sticky="NW")
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

        self.b_axis_on = tk.Button(self.plot_2D_frame, text="Axis On", command=self.callback_axis_on_2D_button)
        self.b_axis_on.config(width=8)
        self.b_axis_on.grid(row=5, column=0, sticky="NW")
        self.b_axis_off = tk.Button(self.plot_2D_frame, text="Axis Off", command=self.callback_axis_off_2D_button)
        self.b_axis_off.config(width=8)
        self.b_axis_off.grid(row=5, column=1, sticky="NW")

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

        if self.fig_3D == None:
            self.fig_3D = plt.figure(103)
            self.ax_3D = self.fig_3D.add_subplot(projection='3d')
            self.fig_3D.suptitle("Pole figure 3D: ", fontsize=16)
            self.fig_3D.canvas.mpl_connect('close_event', self.on_close_3D_fig)

        self.ax_3D.cla()

        Thetas = np.array(self.get_thetas(self.file_data[0]))
        # ____________
        Azimuths = np.array(self.get_azimuths())
        # ____________
        Z = np.array(self.get_z_values())

        #print("Thetas: ", len(Thetas), "Azimuths: ", len(Azimuths), "Z: ", len(Z))

        Thetas_2D_array, Azimuths_2D_array = np.meshgrid(np.radians(Thetas), Azimuths)

        X = Azimuths_2D_array * np.cos(Thetas_2D_array)
        Y = Azimuths_2D_array * np.sin(Thetas_2D_array)

        self.fig_3D.suptitle(self.Entry_3D_plot_label.get_value(), fontsize=16)

        self.ax_3D.plot_surface(X, Y, Z, cmap='jet', alpha=0.75)
        #self.ax_3D.set_axis_off()


    def callback_update_axis_2D_button(self):
        Thetas = range(0, 360, int(self.Entry_theta_spacing.get_value()))
        self.ax_2D.set_xticks(np.radians(Thetas))

        Small_Chi = self.label_container.get_first_entry().get_value()
        Large_Chi = self.label_container.get_last_entry().get_value()
        Chis = range(int(Small_Chi), int(Large_Chi), int(self.Entry_Chi_spacing.get_value()))
        self.ax_2D.set_yticks(Chis)
        plt.show()

    def callback_test_2D_button(self):
        print("Test button")  # Keep this line

    def callback_axis_on_2D_button(self):
        self.ax_2D.set_axis_on()
        plt.show()

    def callback_axis_off_2D_button(self):
        self.ax_2D.set_axis_off()
        plt.show()

    def on_close_2D_fig(self, event):
        print("closed window")
        self.fig_2D = None
        self.ax_2D = None

    def plot_2D(self):

        if self.fig_2D == None:
            self.fig_2D, self.ax_2D = plt.subplots(num=102, subplot_kw={'projection': 'polar'})
            self.fig_2D.suptitle("Pole figure 2D: ", fontsize=16)
            self.fig_2D.canvas.mpl_connect('close_event', self.on_close_2D_fig)

        self.ax_2D.cla()
        # ____________
        Thetas = np.array(self.get_thetas(self.file_data[0]))
        # ____________
        Azimuths = np.array(self.get_azimuths())
        # ____________
        Values = np.array(self.get_z_values())

        print("Thetas: ", len(Thetas), "Azimuths: ", len(Azimuths), "Values: ", len(Values))

        print(Values)

        # Create 2D-arrays of polar coordinates
        theta_, asimuths_ = np.meshgrid(np.radians(Thetas), Azimuths)

        print("Values shape: ", Values.shape)
        print("Theta shape: ", Thetas.shape)
        print("Azimuth shape", Azimuths.shape)

        cax = self.ax_2D.contourf(theta_, asimuths_, Values, 75, cmap='jet')
        self.ax_2D.set_theta_zero_location("N")
        self.ax_2D.set_theta_direction(-1)
        cb = self.fig_2D.colorbar(cax, pad=0.15)
        cb.set_label(self.get_2d_counts_label())

        self.fig_2D.suptitle(self.Entry_2D_plot_label.get_value(), fontsize=16)

        self.callback_update_axis_2D_button()

    def get_z_values(self):
        temp_values = []

        for file in range(self.no_files_index):
            Temp_list = []
            if self.plot_selection_index == 0 : # lin
                Temp_list = self.file_data[file].get_col2_in_linear_with_offset(0)
            elif self.plot_selection_index == 1 :# log
                Temp_list = self.file_data[file].get_col2_in_log_with_offset(0)
            elif self.plot_selection_index == 2 :
                Temp_list = self.file_data[file].get_col2_in_sqrt_with_offset(0)

            temp_values.append(Temp_list)

        return temp_values

    def get_azimuths(self):
        return self.label_container.get_list_of_all_entry_values()

    def get_thetas(self, file_container):
        temp_thetas = []
        for element in file_container.get_col1():
            temp_thetas.append(element)
        # temp_thetas.append(360) ## For closed circle
        return temp_thetas

    def get_2d_counts_label(self):
        ret_val = ""
        if self.plot_selection_index == 0: #lin
            ret_val = "Counts"
        elif self.plot_selection_index == 1: #log
            ret_val = "Log(Counts)"
        elif self.plot_selection_index == 2:  # sqrt
            ret_val = "Sqrt(Counts)"
        return ret_val


    def callback_calculate_button(self):
        self.results.clear_results() # Reset result content!

        # Extract data from the file contents including the entry...
        for file in range(self.no_files_index):
            Phi = self.file_data[file].Column1
            Lin_Intensity = self.file_data[file].get_col2_in_linear_with_offset(0)
            Log_Intensity = self.file_data[file].get_col2_in_log_with_offset(0)
            sqrt_Intensity = self.file_data[file].get_col2_in_sqrt_with_offset(0)
            Chi = self.label_container.get_entry_value(file)

            # Write the data to csv-file!
            for index in range(len(Phi)):
                self.results.add_row_5(Phi[index], Chi, Lin_Intensity[index], Log_Intensity[index],
                                       sqrt_Intensity[index], 2, ",")


        self.o_text_plotter.plot_Pole_text(self.results.get_list())

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns()
        self.file_data.append(data)

        self.label_container.add_float_entry(data.file_name, self.Entry_Chi.get_value())

    def callback_import_all_button(self):

        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns()
            self.file_data.append(data_in_file)

            self.label_container.add_float_entry(data_in_file.file_name, self.Entry_Chi.get_value() * (self.no_files_index - 1))

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
