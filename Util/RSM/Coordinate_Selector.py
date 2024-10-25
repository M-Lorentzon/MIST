import tkinter as tk
import Util.Definitions as Defs

class Coordinate_Selector:

    def __init__(self, master, init_color, row_, col_, colspan=1):
        self.master = master
        self.row_ = row_
        self.col_ = col_
        self.colspan = colspan

        self.widget_frame = tk.Frame(self.master)
        self.widget_frame.grid(row=self.row_, column=self.col_, columnspan=self.colspan, sticky="NW")

        self.dropvar = tk.StringVar(self.widget_frame, init_color)

        self.coordinates = {"MgO 200", "MgO 400", "MgO 4-20", "MgO 420", "MgO 311", "MgO 3-1-1", "HfN 200", "HfN 400", "HfN 311", "HfN 3-1-1", "HfN 420", "HfN 4-20"}

        self.droplist = tk.OptionMenu(self.widget_frame, self.dropvar, *self.coordinates)
        self.droplist.config(bg=Defs.c_color_selector)
        self.droplist["menu"].config(bg=Defs.c_color_selector)
        self.droplist.grid()

        self.dropvar.trace("w", self.change_dropvar)


    def change_dropvar(self, *args):
        print(self.dropvar.get())

    def get_selected_coordinates(self):
        Selection = self.dropvar.get()
        retval = (0, 0) # (omega, 2theta)

        if Selection == "MgO 200":
            retval = (21.4589,42.9178)
        elif Selection == "MgO 400":
            retval = (47.0265, 94.053)
        elif Selection == "MgO 311":
            retval = (12.1094,74.6977)
        elif Selection == "MgO 3-1-1":
            retval = (62.5882,74.6977)
        elif Selection == "MgO 420":
            retval = (28.3904, 109.911)
        elif Selection == "MgO 4-20":
            retval = (81.5205, 109.911)

        elif Selection == "HfN 200":
            retval = (19.9737,39.9474)
        elif Selection == "HfN 400":
            retval = (43.0935, 86.187)
        elif Selection == "HfN 311":
            retval = (9.2644,69.0075)
        elif Selection == "HfN 3-1-1":
            retval = (59.7432,69.0075)
        elif Selection == "HfN 420":
            retval = (23.2366,99.6034)
        elif Selection == "HfN 4-20":
            retval = (76.3667,99.6034)

        return retval
