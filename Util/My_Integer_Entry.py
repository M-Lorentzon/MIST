import tkinter as tk
import Util.Definitions as Defs

class My_Integer_Entry:

    def __init__(self, master, label, start_val, row_, col_, colspan=1):
        self.master_frame = master
        self.widget_frame = tk.Frame(self.master_frame)
        self.widget_frame.grid(row=row_, column=col_, columnspan=colspan, sticky="W")

        # Data
        self.Entry_value = 0

        # make label
        self.label = tk.Label(self.widget_frame, text=label)
        self.label.grid(row=0, column=0, sticky="W")
        self.label.config(bg=Defs.c_float_entry, borderwidth=1, padx=2, pady=2)

        # make the entry
        self.Entry = tk.Entry(self.widget_frame, width=5)
        self.Entry.grid(row=0, column=1, sticky="W")
        self.Entry.insert(0, str(start_val))

    def set_label_bg(self, color):
        self.label.config(bg=color)

    def set_entry_width(self, width):
        self.Entry.config(width=width)

    def get_value(self):
        value = self.Entry.get()

        try:
            self.Entry_value = int(value)
            self.good_input()
        except ValueError:
            self.bad_input()

        return self.Entry_value

    def bad_input(self):
        self.Entry.config(fg=Defs.c_error_text)

    def good_input(self):
        self.Entry.config(fg=Defs.c_good_text)

    def hide(self):
        self.label.grid_forget()
        self.Entry.grid_forget()

    def set_entry_value(self, val):
        self.Entry_value = val
        self.Entry.delete(0, tk.END)
        self.Entry.insert(0, str(val))
