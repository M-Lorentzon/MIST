import tkinter as tk

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
from Util.My_Toggle_Switch import My_Toggle_Switch

import tkscrolledframe as SF
import Util.Definitions as Defs
import matplotlib.pyplot as plt

Description = """This script is a tool for ...

Helping others with their scripts
"""

class Plugin_Help_Others:

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

        # Master label
        self.label = tk.Label(self.my_frame, text="Help Others", bg=Defs.c_script_name)
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
        self.selection_index = 0
        self.b_linear = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=5, column=0, sticky="NW")
        self.b_log = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=5, column=1, sticky="NW")
        self.callback_linear_button()

        self.b_legend = My_Toggle_Switch(self.select_button_frame, "Legend", 5,2)
        self.b_black_lines = My_Toggle_Switch(self.select_button_frame, "Black lines", 5, 3)

        # Entries
        self.Entry_offset = My_Float_Entry(self.entry_frame, "Multi-graph offset", 1, 1, 0)

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
            self.fig_stack, self.ax_stack = plt.subplots(num=100)
            self.fig_stack.canvas.mpl_connect('close_event', self.on_close)

        self.ax_stack.cla()

        Number_of_graphs = len(self.file_data)

        for file_index in range(len(self.file_data)):
            label = self.data_labels[file_index].get_value()
            offset = self.Entry_offset.get_value() * (Number_of_graphs - file_index)
            x_val = self.file_data[file_index].Column1
            y_val = self.file_data[file_index].get_col2_in_linear_with_offset(offset)
            y_val_log = self.file_data[file_index].get_col2_in_log_with_offset(offset)


            if self.selection_index == 0:  # linear
                self.ax_stack.plot(x_val, y_val, label=label)
                self.ax_stack.set_ylabel("Intensity (linear, a.u)")
            elif self.selection_index == 1:  # log
                self.ax_stack.plot(x_val, y_val_log, label=label)
                self.ax_stack.set_ylabel("Intensity (log10, a.u)")
            else:
                print("Error in selecting lin, log")

        if self.b_legend.is_on():
            self.ax_stack.legend()
            self.ax_stack.legend().set_draggable(True)

        if self.b_black_lines.is_on():
            for line in self.ax_stack.get_lines():
                line.set_color('black')

        self.ax_stack.set_xlabel("Binding Energy (eV)")

        self.ax_stack.invert_xaxis()

        self.fig_stack.show()

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

    def callback_import_all_button(self):
        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns_help_Pambu()
            self.file_data.append(data_in_file)

            new_entry = My_Label_Entry(self.label_entry_frame, data_in_file.file_name, self.no_files_index, 0)
            new_entry.set_label_bg("seagreen1")
            new_entry.set_entry_value(data_in_file.file_name)
            self.data_labels.append(new_entry)

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns_help_Pambu()
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels :
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()