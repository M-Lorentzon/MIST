import tkinter as tk
from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
import Util.Definitions as Defs
import matplotlib.pyplot as plt
import tkscrolledframe as SF

Description = """This script treats ___ data
and produce _____ 

"""

class Plugin_Nanoindent:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler  # to get data from

        self.active = False
        self.savable_script = False

        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries) # Master within this scope

        self.sframe = SF.ScrolledFrame(self.my_frame, width=370, height=400)
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

        # Master label
        self.label = tk.Label(self.my_frame, text="Nanoindentation settings", bg=Defs.c_script_name)
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
        self.b_import_all = tk.Button(self.master_button_frame, text="Import all",
                                      command=self.callback_import_all_button)
        self.b_import_all.config(width=8)
        self.b_import_all.grid(row=0, column=1, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files",
                                       command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=2, sticky="NW")
        self.b_calculate = tk.Button(self.master_button_frame, text="Calculate", command=self.callback_calculate_button)
        self.b_calculate.config(width=8)
        self.b_calculate.grid(row=0, column=3, sticky="NW")
        self.b_plot = tk.Button(self.master_button_frame, text="Plot", command=self.callback_plot_button)
        self.b_plot.config(width=8)
        self.b_plot.grid(row=0, column=4, sticky="NW")


        # Entries
        self.Entry____ = My_Float_Entry(self.entry_frame, "___", 600, 2, 0)

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

        # Calculated data in string .csv format
        self.results = []

        self.fig_indent, self.ax_indent = plt.subplots(num=104)
        plt.close(self.fig_indent)

    def callback_plot_button(self):
        plt.close(self.fig_indent)
        self.fig_indent, self.ax_indent = plt.subplots(num=104)
        for index, data in enumerate(self.file_data) :
            depths = data.get_col1()
            loads = data.get_col2()
            label = self.data_labels[index].get_value()

            self.ax_indent.plot(depths, loads, label=label)

        self.fig_indent.suptitle("Load/Unload curves", fontsize=16)
        self.ax_indent.set_xlabel("Depth [nm]")
        self.ax_indent.set_ylabel("Force [uN]")
        self.ax_indent.legend()
        self.ax_indent.legend().set_draggable(True)
        self.fig_indent.show()


    def callback_calculate_button(self):
        pass

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns(5)
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def callback_import_all_button(self):

        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns(5)
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


    def update(self, Angle, intensity):
        self.Angle_Col = Angle
        self.Intensity_col = intensity

        # Update results with list of strings.
        # self.results = 'script function'

    def get_results(self):
        return self.results

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()



