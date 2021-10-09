import tkinter as tk
import Util.Definitions as Defs

class My_Label_Entry:

    def __init__(self, master, label, row_, col_, colspan=1):
        self.master_frame = master
        self.widget_frame = tk.Frame(self.master_frame)
        self.widget_frame.grid(row=row_, column=col_, columnspan=colspan)

        # Data
        self.Entry_value = ""

        # make label
        self.label = tk.Label(self.widget_frame, text=label)
        self.label.grid(row=0, column=0)
        self.label.config(bg=Defs.c_label_entry, borderwidth=1, padx=2, pady=2)

        # make the entry
        self.Entry = tk.Entry(self.widget_frame, width=30)
        self.Entry.grid(row=0, column=1)
        self.Entry.insert(0, "?")

    def get_value(self):
        self.Entry_value = self.Entry.get()
        return self.Entry_value

    def set_entry_value(self, string_):
        self.Entry.delete(0, tk.END)
        self.Entry.insert(0, string_)

    def set_label_bg(self, color):
        self.label.config(bg=color)

    def hide(self):
        self.label.grid_forget()
        self.Entry.grid_forget()


