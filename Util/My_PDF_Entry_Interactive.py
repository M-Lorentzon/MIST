import tkinter as tk
import Util.Definitions as Defs
import Util.My_PDF_Card_Entry as PDF_Entry
import Util.My_Checkbutton as checkbox

class My_PDF_Entry_Interactive:

    def __init__(self, master, peak, twotheta, intensity, row_, col_):
        self.master_frame = master
        self.widget_frame = tk.Frame(self.master_frame)
        self.widget_frame.grid(row=row_, column=col_)
        self.row_ = row_
        self.col_ = col_

        self.my_checkbox = checkbox.My_Checkbutton(self.widget_frame, self.function_pointer_checkbox, "Activate", 0, 0)
        self.my_checkbox.set_checkbutton_layout_two()
        self.my_pdf_entry = PDF_Entry.My_PDF_Card_Entry(self.widget_frame, peak, twotheta, intensity, 0, 1)


    def function_pointer_checkbox(self):
        pass

    def set_is_active(self):
        self.my_checkbox.checkbutton.set(1)

    def hide_entry(self):
        self.widget_frame.grid_forget()

    def show_entry(self):
        self.widget_frame.grid(row=self.row_, column=self.col_)

    def get_entry(self):
        return self.my_pdf_entry

    def get_checkbutton(self):
        return self.my_checkbox

