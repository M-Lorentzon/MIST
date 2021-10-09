import tkinter as tk
import Util.Definitions as Defs

class My_Checkbutton:

    def __init__(self, master_frame, function_pointer, button_text, row_, col_):
        self.master_frame = master_frame
        self.function_pointer = function_pointer
        self.row_ = row_
        self.col_ = col_
        self.button_text = button_text

        self.checkbutton = tk.IntVar()
        self.checkbutton.trace('w', self.callback_checkbutton)
        self.Button = tk.Checkbutton(self.master_frame, text=self.button_text,
                                     variable=self.checkbutton,
                                     onvalue=1, offvalue=0,
                                     height=2, width=10)
        self.Button.grid(row=self.row_, column=self.col_)

        self.most_recent_selected = False
        self.most_recent_deselected = False

    def callback_checkbutton(self, *args):
        if self.checkbutton.get() == 1:
            self.most_recent_selected = True
        else:
            self.most_recent_deselected = True
        self.function_pointer()

    def check_handled(self):
        self.most_recent_selected = False
        self.most_recent_deselected = False

    def is_active(self):
        retval = False
        if self.checkbutton.get() == 1:
            retval = True
        return retval

    def set_text(self, text):
        self.Button.config(text=text)

    def set_checkbutton_layout_one(self):
        self.Button.config(height=2, width=10,
                           bg=Defs.c_pdf_setting_button_accepted)

    def set_checkbutton_layout_two(self):
        self.Button.config(height=1, width=10,
                           bg=Defs.c_pdf_setting_button_all)
