import tkinter as tk
import Util.Definitions as Defs
from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
from Util.color_selector import Color_Selector
import tkscrolledframe as SF
import matplotlib.pyplot as plt


Description = """This script is used for plotting
and converting XPS-data

"""

class Plugin_XPS_data:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler
        self.my_frame = tk.Frame(self.script_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)

        self.active = False
        self.savable_script = True

        self.sframe = SF.ScrolledFrame(self.my_frame, width=400, height=250)
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
        self.add_line_to_plot_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.add_line_to_plot_frame.grid(row=5, column=0)

        # Label
        self.label = tk.Label(self.my_frame, text="XPS data plotting and converting", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Entries
        self.Entry_offset = My_Float_Entry(self.entry_frame, "Multi-graph offset", 2000, 1, 0)
        self.Entry_Line_Thickn = My_Float_Entry(self.entry_frame, "Graph line thickness", 0.5, 1, 1)
        self.Entry_title = My_Label_Entry(self.entry_frame, "Title", 0, 0, 4)

        self.b_legend = tk.Button(self.entry_frame, text="legend", command=self.callback_enable_legend)
        self.b_legend.config(width=8)
        self.b_legend.grid(row=2, column=0)
        self.legend_enabled = True
        self.callback_enable_legend()

        self.xaxis_is_binding = True
        self.b_xaxis_binding = tk.Button(self.entry_frame, text="Binding", command=self.callback_binding_energy)
        self.b_xaxis_binding.config(width=8)
        self.b_xaxis_binding.grid(row=2, column=1)
        self.b_xaxis_kinetic = tk.Button(self.entry_frame, text="Kinetic", command=self.callback_kinetic_energy)
        self.b_xaxis_kinetic.config(width=8)
        self.b_xaxis_kinetic.grid(row=2, column=2)
        self.callback_binding_energy()

        self.b_black_lines = tk.Button(self.entry_frame, text="black lines", command=self.callback_black_lines)
        self.b_black_lines.config(width=8)
        self.b_black_lines.grid(row=2, column=3)
        self.use_black_lines = True
        self.callback_black_lines()


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

        # 'Add line to plot' stuff
        self.b_add_line1 = tk.Button(self.add_line_to_plot_frame, text="Add line", command=self.callback_add_line1)
        self.b_add_line1.grid(row=1, column=0, sticky="NW")
        self.Entry_line_x_pos1 = My_Float_Entry(self.add_line_to_plot_frame, "x-pos", 70, 1, 1)
        self.Entry_line_y_height1 = My_Float_Entry(self.add_line_to_plot_frame, "height", 40000, 1, 2)
        self.Entry_line_thickness1 = My_Float_Entry(self.add_line_to_plot_frame, "Thickn", 0.02, 1, 3)
        self.Entry_line_color1 = Color_Selector(self.add_line_to_plot_frame, "black", 1, 4)

        self.b_add_line2 = tk.Button(self.add_line_to_plot_frame, text="Add line", command=self.callback_add_line2)
        self.b_add_line2.grid(row=2, column=0, sticky="NW")
        self.Entry_line_x_pos2 = My_Float_Entry(self.add_line_to_plot_frame, "x-pos", 70, 2, 1)
        self.Entry_line_y_height2 = My_Float_Entry(self.add_line_to_plot_frame, "height", 40000, 2, 2)
        self.Entry_line_thickness2 = My_Float_Entry(self.add_line_to_plot_frame, "Thickn", 0.02, 2, 3)
        self.Entry_line_color2 = Color_Selector(self.add_line_to_plot_frame, "black", 2, 4)

        ##################################################
        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

        self.fig_stack = None
        self.ax_stack = None

##################################################
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

        Number_of_graphs = len(self.file_data)

        if self.xaxis_is_binding:
            for file_index in range(len(self.file_data)):
                binding_E = self.file_data[file_index].get_col4()
                # counts = self.file_data[file_index].get_col2()
                cps = self.file_data[file_index].get_col5()
                label = self.data_labels[file_index].get_value()
                offset = self.Entry_offset.get_value() * (Number_of_graphs - file_index)
                Line_thickness = self.Entry_Line_Thickn.get_value()

                self.ax_stack.plot(binding_E, self.get_value_with_offset(cps, offset), label=label, linewidth=Line_thickness)

            self.ax_stack.set_ylabel("cps (a.u)")
            self.ax_stack.set_xlabel("Binding energy [eV]")
            self.ax_stack.invert_xaxis()

        else:
            for file_index in range(len(self.file_data)):
                kinetic_E = self.file_data[file_index].get_col1()
                # counts = self.file_data[file_index].get_col2()
                cps = self.file_data[file_index].get_col5()
                label = self.data_labels[file_index].get_value()
                offset = self.Entry_offset.get_value() * (Number_of_graphs - file_index)
                Line_thickness = self.Entry_Line_Thickn.get_value()

                self.ax_stack.plot(kinetic_E, self.get_value_with_offset(cps, offset), label=label, linewidth=Line_thickness)

            self.ax_stack.set_ylabel("cps (a.u)")
            self.ax_stack.set_xlabel("Kinetic energy [eV]")

        self.fig_stack.suptitle(self.Entry_title.get_value())
        if self.legend_enabled:
            self.ax_stack.legend()
            self.ax_stack.legend().set_draggable(True)

        if self.use_black_lines:
            for line in self.ax_stack.get_lines():
                line.set_color('black')

        self.fig_stack.show()

    def callback_calculate_button(self):
        pass

    def callback_import_button(self):
        ignore_rows = 7
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns(ignore_rows)
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def callback_import_all_button(self):
        ignore_rows = 7
        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns(ignore_rows)
            self.file_data.append(data_in_file)

            new_entry = My_Label_Entry(self.label_entry_frame, data_in_file.file_name, self.no_files_index, 0)
            new_entry.set_entry_value(data_in_file.file_name)
            new_entry.set_label_bg("seagreen1")
            self.data_labels.append(new_entry)

    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels :
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []

##################################################
    # help functions
    def get_value_with_offset(self, values, offset):
        retval = []
        for elem in values:
            retval.append(elem + offset)
        return retval
##################################################
    def callback_enable_legend(self):
        if self.legend_enabled:
            self.legend_enabled = False
            self.b_legend.config(bg=Defs.c_button_inactive)
        else:
            self.legend_enabled = True
            self.b_legend.config(bg=Defs.c_button_active)

    def callback_black_lines(self):
        if self.use_black_lines:
            self.use_black_lines = False
            self.b_black_lines.config(bg=Defs.c_button_inactive)
        else:
            self.use_black_lines = True
            self.b_black_lines.config(bg=Defs.c_button_active)

    def callback_binding_energy(self):
        self.b_xaxis_binding.config(bg=Defs.c_button_active)
        self.b_xaxis_kinetic.config(bg=Defs.c_button_inactive)
        self.xaxis_is_binding = True

    def callback_kinetic_energy(self):
        self.b_xaxis_binding.config(bg=Defs.c_button_inactive)
        self.b_xaxis_kinetic.config(bg=Defs.c_button_active)
        self.xaxis_is_binding = False

    def callback_add_line1(self):
        xval = self.Entry_line_x_pos1.get_value()
        yval = self.Entry_line_y_height1.get_value()
        text = str(xval)
        color = self.Entry_line_color1.get_color()
        line_thickness = self.Entry_line_thickness1.get_value()
        self.ax_stack.bar(xval, height=yval, width=line_thickness, color=color)
        self.ax_stack.text(xval, yval-1, text, {'ha': 'right'}, rotation=90, color=color)
        self.fig_stack.show()

    def callback_add_line2(self):
        xval = self.Entry_line_x_pos2.get_value()
        yval = self.Entry_line_y_height2.get_value()
        text = str(xval)
        color = self.Entry_line_color2.get_color()
        line_thickness = self.Entry_line_thickness2.get_value()
        self.ax_stack.bar(xval, height=yval, width=line_thickness, color=color)
        self.ax_stack.text(xval, yval-1, text, {'ha': 'right'}, rotation=90, color=color)
        self.fig_stack.show()

##################################################
##################################################
    def update(self, Angle, intensity):
        pass

    def get_results(self):
        pass

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()

