import tkinter as tk
import Util.Definitions as Defs

class Color_Scheme_Selector:

    def __init__(self, master, init_color, row_, col_, colspan=1):
        self.master = master
        self.row_ = row_
        self.col_ = col_
        self.colspan = colspan

        self.widget_frame = tk.Frame(self.master)
        self.widget_frame.grid(row=self.row_, column=self.col_, columnspan=self.colspan, sticky="NW")

        self.dropvar = tk.StringVar(self.widget_frame, init_color)

        self.colors = {"jet", "viridis", "gray", "coolwarm", "plasma", "cividis", "gist_earth", "BrBG_r", "gnuplot", "copper", "copper_r", "ocean_r", "Greys", "winter", "winter_r"}

        self.droplist = tk.OptionMenu(self.widget_frame, self.dropvar, *self.colors)
        self.droplist.config(bg=Defs.c_color_selector)
        self.droplist["menu"].config(bg=Defs.c_color_selector)
        self.droplist.grid()

        self.dropvar.trace("w", self.change_dropvar)


    def change_dropvar(self, *args):
        print(self.dropvar.get())

    def get_color(self):
        return self.dropvar.get()