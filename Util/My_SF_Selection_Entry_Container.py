import tkinter as tk
import tkscrolledframe as SF
import Util.Definitions as Defs

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry


class My_SF_Selection_Entry_Container:

    def __init__(self, master, width, height, _row, _col):

        self.master_frame = master
        self.my_frame = tk.Frame(self.master_frame, bg=Defs.c_script_entries)
        self.my_frame.grid(row=_row, column=_col)

        self.sframe = SF.ScrolledFrame(self.my_frame, width=width, height=height)
        self.sframe.grid(row=10, column=0, columnspan=3)
        self.sframe.config(bg=Defs.c_frame_color)
        self.sframe.bind_arrow_keys(self.my_frame)
        self.sframe.bind_scroll_wheel(self.my_frame)

        self.label_entry_frame = self.sframe.display_widget(tk.Frame)
        self.label_entry_frame.config(bg=Defs.c_frame_color)

        self.b_next = tk.Button(self.my_frame, text="-->", command=self.callback_next_file)
        self.b_next.config(bg=Defs.c_black, fg=Defs.c_white)
        self.b_next.grid(row=0, column=2, sticky="E", columnspan=5)
        self.b_prev = tk.Button(self.my_frame, text="<--", command=self.callback_prev_file)
        self.b_prev.config(bg=Defs.c_black, fg=Defs.c_white)
        self.b_prev.grid(row=0, column=0, sticky="W")

        self.index_max = -1
        self.index_current_highlight = -1
        self.entries = []


    def callback_prev_file(self):
        if self.index_current_highlight != 0 :
            self.index_current_highlight -= 1
        self.highlight_active_file()

    def callback_next_file(self):
        no_files = len(self.entries)
        if self.index_current_highlight >= no_files - 1:
            return
        else:
            self.index_current_highlight += 1

        self.highlight_active_file()

    def highlight_active_file(self):
        # Highlight active file!
        for element in self.entries:
            element.set_label_bg(Defs.c_file_inactive)

        if len(self.entries) != 0:
            self.entries[self.index_current_highlight].set_label_bg(Defs.c_file_active)


    def add_float_entry(self, label, value):
        self.index_max += 1

        new_entry = My_Float_Entry(self.label_entry_frame, label, value, self.index_max, 0)
        new_entry.set_label_bg("seagreen1")

        self.entries.append(new_entry)

        if self.index_max >= 0:
            self.index_current_highlight = 0

    def get_all_entries(self):
        return self.entries

    def get_selected_entry(self):
        if len(self.entries) != 0:
            return self.entries[self.index_current_highlight]
        else :
            return False

    def get_list_of_all_entry_values(self):
        tmp = []
        for element in self.entries:
            tmp.append(element.get_value())
        return tmp

    def get_entry_value(self, index):
        return self.entries[index].get_value()

    def get_first_entry(self):
        return self.entries[0]

    def get_last_entry(self):
        return self.entries[self.index_max]

    def remove_all_entries(self):
        self.index_current_highlight = -1
        self.index_max = -1
        for entry in self.entries:
            entry.hide()
        self.entries = []

    def remove_selected_entry(self):
        pass






