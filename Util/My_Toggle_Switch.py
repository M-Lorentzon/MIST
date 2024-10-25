import tkinter as tk
import Util.Definitions as Defs

class My_Toggle_Switch:

    def __init__(self, master_frame, button_text, row_, col_):
        self.master_frame = master_frame
        self.row_ = row_
        self.col_ = col_
        self.button_text = button_text

        self.Button = tk.Button(self.master_frame, text=self.button_text, command=self.callback_toggle)
        self.Button.grid(row=self.row_, column=self.col_)
        self.Button.config(bg=Defs.c_button_inactive)

        self.toggle_on = False

    def callback_toggle(self):
        if self.toggle_on:
            self.Button.config(bg=Defs.c_button_inactive)
            self.toggle_on = False
        else:
            self.Button.config(bg=Defs.c_button_active)
            self.toggle_on = True

    def is_on(self):
        return self.toggle_on

    def set_text(self, text):
        self.Button.config(text=text)
