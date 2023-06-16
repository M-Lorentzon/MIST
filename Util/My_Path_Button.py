import tkinter as tk
import tkinter.filedialog as filedialog
import Util.Definitions as Defs

class My_Path_Button:

    def __init__(self, master, label, is_file, row_, col_, colspan=1):
        self.master_frame = master
        self.widget_frame = tk.Frame(self.master_frame)
        self.widget_frame.grid(row=row_, column=col_, columnspan=colspan)

        self.is_file = is_file

        # Data
        self.Entry_value = ""

        # Make button
        self.button = tk.Button(self.widget_frame, text=label, command=self.callback_button)
        self.button.grid(row=0, column=0, sticky="NW")

        # make the entry
        self.Entry = tk.Entry(self.widget_frame, width=120)
        self.Entry.grid(row=0, column=1)
        self.Entry.insert(0, "?")

    def callback_button(self):
        file_path = ""
        if self.is_file:
            file_path = filedialog.askopenfilename()
        else:
            file_path = filedialog.askdirectory()

        self.set_entry_value(file_path)

    def get_value(self):
        self.Entry_value = self.Entry.get()
        return self.Entry_value

    def set_entry_value(self, string_):
        self.Entry.delete(0, tk.END)
        self.Entry.insert(0, string_)

    def hide(self):
        self.button.grid_forget()
        self.Entry.grid_forget()


