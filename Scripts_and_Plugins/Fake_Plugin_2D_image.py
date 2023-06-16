import tkinter as tk

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry

import tkscrolledframe as SF
import Util.Definitions as Defs

Description = """This script is a tool for ...

"""

class Plugin_2D_Image:

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
        self.label = tk.Label(self.my_frame, text="XRD stacked lines settings", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Master description text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

    def callback_import_all_button(self):
        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns()
            self.file_data.append(data_in_file)

            new_entry = My_Label_Entry(self.label_entry_frame, data_in_file.file_name, self.no_files_index, 0)
            new_entry.set_label_bg("seagreen1")
            new_entry.set_entry_value(data_in_file.file_name)
            self.data_labels.append(new_entry)

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns()
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()