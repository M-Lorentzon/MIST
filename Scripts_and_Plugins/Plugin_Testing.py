import math
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import numpy as np
from scipy.optimize import curve_fit
import lmfit as lmfit

import Util.Function_definitions as func_defs



from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry

import tkscrolledframe as SF
import Util.Definitions as Defs

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

Description = """This is a test script

"""

class Plugin_Testing:

    def __init__(self, Script_frame, file_handler, error_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler # to get data from
        self.o_error_handler = error_handler

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
        self.master_button_frame.grid(row=2, column=0)
        self.select_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.select_button_frame.grid(row=3, column=0)
        self.options_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.options_frame.grid(row=4, column=0)
        self.display_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.display_frame.grid(row=8, column=0)
        self.entry_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.entry_frame.grid(row=9, column=0)

        # Master label
        self.label = tk.Label(self.my_frame, text="Testing script", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Master description text
        self.text = tk.Text(self.my_frame, width=50, height=10, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        ## Master buttons
        self.b_import = tk.Button(self.master_button_frame, text="Import", command=self.callback_import_button)
        self.b_import.config(width=8)
        self.b_import.grid(row=0, column=0, sticky="NW")
        self.b_plot = tk.Button(self.master_button_frame, text="Plot", command=self.callback_plot_button)
        self.b_plot.config(width=8)
        self.b_plot.grid(row=0, column=2, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files", command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=3, sticky="NW")
        self.b_test = tk.Button(self.master_button_frame, text="test", command=self.callback_testing)
        self.b_test.config(width=8)
        self.b_test.grid(row=0, column=4, sticky="NW")

        # Selection buttons
        self.selection_index = 1
        self.b_linear = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=5, column=0, sticky="NW")
        self.b_log = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=5, column=1, sticky="NW")
        self.callback_log_button()

        # Options buttons etc.
        self.b_print_details = tk.Button(self.options_frame, text="model details", command=self.callback_print_model_details)
        self.b_print_details.grid(row= 0, column=0, sticky="NW")

        # Result text and other stuff for results
        self.result_text = ScrolledText(self.display_frame, width=45, height=8)
        self.result_text.grid(row=0, column=0, columnspan=5)
        self.result_text.insert(0.0, "Calculated results: ")
        self.result_text.config(state='normal')
        self.line_index = 0

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = None
        self.data_labels = None
        self.x_axis = None
        self.y_axis = None
        self.y_axis_log = None


        self.fig = None
        self.ax = None

        self.clicked_select_counter = 0
        self.clicked_point_coordinates = []
        self.clicked_redraw = False
        self.fig_select_button = None
        self.ax_select = None
        self.cid_select_points = None

        self.fig_ok_button = None
        self.ax_ok = None
        self.fig_model_button = None
        self.ax_model = None

        self.fit_result = None # lmfit: ModelResult object
        self.model_x_axis = None


    def on_close(self, event):
        print("closed window")
        self.fig = None
        self.ax = None

    def on_click_in_graph(self, event):
        self.clicked_select_counter += 1
        self.clicked_redraw = True

        if self.clicked_select_counter > 3:
            self.fig.canvas.mpl_disconnect(self.cid_select_points)
            #print(self.clicked_point_coordinates)

        else:
            click_x, click_y = event.xdata, event.ydata

            idx = np.searchsorted(self.x_axis, click_x, side='left')
            x_val = self.x_axis[idx]
            y_val = self.y_axis[idx]
            self.clicked_point_coordinates.append((x_val, y_val))

            if self.clicked_select_counter == 1 : #First point at peak top

                if self.selection_index == 0: # Linear
                    self.ax.plot(x_val, y_val, marker='*', markersize=15, color='red')
                elif self.selection_index == 1: # Log
                    self.ax.plot(x_val, math.log10(y_val), marker='*', markersize=15, color='red')
            else:
                if self.selection_index == 0: # Linear
                    self.ax.plot(x_val, y_val, marker='*', markersize=15, color='orange')
                elif self.selection_index == 1: # Log
                    self.ax.plot(x_val, math.log10(y_val), marker='*', markersize=15, color='orange')

            self.fig.show()


    def on_click_select_points(self, event):
        self.clicked_select_counter = 0
        self.cid_select_points = self.fig.canvas.mpl_connect('button_press_event', self.on_click_in_graph)
        self.clicked_point_coordinates.clear()
        if self.clicked_redraw:
            self.callback_plot_button()

    def on_click_plot_model(self, event):

        if self.fit_result is not None:

            if self.selection_index == 0:  # linear
                self.ax.plot(self.model_x_axis, self.fit_result.init_fit, '--', label='initial fit')
                self.ax.plot(self.model_x_axis, self.fit_result.best_fit, '--', label='initial fit')
            elif self.selection_index == 1:  # log
                self.ax.plot(self.model_x_axis, np.log10(self.fit_result.init_fit), '--', label='initial fit')
                self.ax.plot(self.model_x_axis, np.log10(self.fit_result.best_fit), '--', label='initial fit')

            self.fig.legend()
            self.fig.show()

            vals = self.fit_result.params.valuesdict()
            Peak_pos = round(vals['center'], 4)
            self.print_results("Peak pos " + str(Peak_pos))

        else:
            self.print_results("Select peak to model first")

    def on_click_ok_button(self, event):
        if len(self.clicked_point_coordinates) == 3:
            print("Got three points to work with :) ")
            self.fit_gaussian_to_data()
        else:
            self.o_error_handler.Write_notification("Select 3 points first...")

    def fit_gaussian_to_data(self):
        sorted_coords = sorted(self.clicked_point_coordinates)
        selected_peak_center = sorted_coords[1][0]
        selected_peak_height = sorted_coords[1][1]

        ix_left = np.searchsorted(self.x_axis, sorted_coords[0][0], side='left')
        ix_right = np.searchsorted(self.x_axis, sorted_coords[2][0], side='left')

        x_axis_to_fit = self.x_axis[ix_left:ix_right]
        y_axis_to_fit = self.y_axis[ix_left:ix_right]
        self.model_x_axis = x_axis_to_fit

        G_model = lmfit.model.Model(self.Gaussian_function) # lmfit: Model object
        G_params = G_model.make_params(amp=selected_peak_height, center=selected_peak_center, sigma={'value': 0.5, 'min':0}) # lmfit: Parameter object
        self.fit_result = G_model.fit(y_axis_to_fit, G_params, x_data=x_axis_to_fit) # lmfit: ModelResult object

        #print(G_model.param_names, G_model.independent_vars)

    def callback_testing(self):
        pass

    def callback_print_model_details(self):
        if self.fit_result is None:
            print("No model results...")
        else:
            print(".params.valuesdict()")
            print(self.fit_result.params.valuesdict())
            print(".fit_result()")
            print(self.fit_result.fit_report())
            print(".summary()")
            print(self.fit_result.summary())

            self.fit_result.plot_residuals()


    def Gaussian_function(self, x_data, amp, center, sigma):
        model = amp * 1 / (np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x_data - center) / sigma) ** 2)
        return model

    def Gaussian_residual(self, params, x_data, y_data):
        vals = params.valuesdict()
        amp = vals['amp']
        center = vals['center']
        sigma = vals['sigma']
        fwhm = vals['fwhm']

        model = amp * 1 / (np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x_data - center) / sigma) ** 2)

        residual = model - y_data
        return residual

    def callback_plot_button(self):
        # First time opening the plot -> Initialize it!
        if self.fig is None:
            self.fig, self.ax = plt.subplots(num=99)
            self.fig.subplots_adjust(bottom=0.2)
            self.fig.canvas.mpl_connect('close_event', self.on_close)

            ## Figure buttons (Use for callbacks)
            # add_axes([xmin,ymin,dx,dy])
            self.ax_select = self.fig.add_axes([0.7, 0.05, 0.1, 0.075])
            self.fig_select_button = Button(self.ax_select, "Select 3", color="lightblue", hovercolor="gold")
            self.fig_select_button.on_clicked(self.on_click_select_points)

            self.ax_ok = self.fig.add_axes([0.8, 0.05, 0.1, 0.075])
            self.fig_ok_button = Button(self.ax_ok, "OK", color="lightblue", hovercolor="gold")
            self.fig_ok_button.on_clicked(self.on_click_ok_button)

            self.ax_model = self.fig.add_axes([0.6, 0.05, 0.1, 0.075])
            self.fig_model_button = Button(self.ax_model, "Model", color="lightblue", hovercolor="gold")
            self.fig_model_button.on_clicked(self.on_click_plot_model)


        self.ax.cla()

        label = self.data_labels.get_value()

        self.x_axis = np.array(self.file_data.Column1)
        self.y_axis = np.array(self.file_data.get_col2())
        self.y_axis_log = np.array(self.file_data.get_col2_in_log_with_offset(0))

        if self.selection_index == 0: # Linear
            self.ax.plot(self.x_axis, self.y_axis, label=label)
            self.ax.set_ylabel("Intensity (linear, a.u)")

        elif self.selection_index == 1: # Log
            self.ax.plot(self.x_axis, self.y_axis_log, label=label)
            self.ax.set_ylabel("Intensity (log, a.u)")

        self.fig.suptitle("blas")
        self.ax.set_xlabel(r"$2\mathrm{\theta \ (^o)} $ ")

        if self.fig_select_button is None:
            pass

        self.fig.show()


    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns()
        self.file_data = data

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, 0, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels = new_entry

    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels :
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []
        self.ax.cla()

    def print_results(self, line):
        self.line_index += 1
        self.result_text.insert("end", "\n")
        self.result_text.insert("end", str(self.line_index)+": ", 'line')
        self.result_text.insert("end", line, 'text')
        self.result_text.tag_config('text', foreground='black')
        self.result_text.tag_config('line', foreground='green')
        self.result_text.yview('end')
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


    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()