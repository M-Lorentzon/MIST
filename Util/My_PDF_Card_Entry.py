import tkinter as tk
import Util.Definitions as Defs

class My_PDF_Card_Entry:

    def __init__(self, master, peak, twotheta, intensity, row_, col_):
        self.master_frame = master
        self.widget_frame = tk.Frame(self.master_frame)
        self.widget_frame.grid(row=row_, column=col_)

        # Data
        self.peak_name = ""
        self.twotheta_value = 0.0
        self.intensity_value = 0.0

        # make label
        self.l_peak = tk.Label(self.widget_frame, text="Peak ID")
        self.l_peak.grid(row=0, column=0)
        self.l_peak.config(bg=Defs.c_PDF_card_entry, borderwidth=1, padx=2, pady=2)
        self.l_2theta = tk.Label(self.widget_frame, text="2theta")
        self.l_2theta.grid(row=0, column=2)
        self.l_2theta.config(bg=Defs.c_PDF_card_entry, borderwidth=1, padx=2, pady=2)
        self.l_intensity = tk.Label(self.widget_frame, text="Int.")
        self.l_intensity.grid(row=0, column=4)
        self.l_intensity.config(bg=Defs.c_PDF_card_entry, borderwidth=1, padx=2, pady=2)

        # make the entry
        self.Entry_Peak = tk.Entry(self.widget_frame, width=10)
        self.Entry_Peak.grid(row=0, column=1)
        self.Entry_Peak.insert(0, peak)
        self.Entry_2theta = tk.Entry(self.widget_frame, width=7)
        self.Entry_2theta.grid(row=0, column=3)
        self.Entry_2theta.insert(0, str(twotheta))
        self.Entry_Intensity = tk.Entry(self.widget_frame, width=4)
        self.Entry_Intensity.grid(row=0, column=5)
        self.Entry_Intensity.insert(0, str(intensity))

    def set_label_bg(self, color):
        self.l_peak.config(bg=color)
        self.l_2theta.config(bg=color)
        self.l_intensity.config(bg=color)

    def get_peak_name(self):
        self.peak_name = self.Entry_Peak.get()
        return self.peak_name

    def get_2theta_value(self):
        value = self.Entry_2theta.get()

        try:
            self.twotheta_value = float(value)
            self.good_2theta_input()
        except ValueError:
            self.bad_2theta_input()

        return self.twotheta_value

    def bad_2theta_input(self):
        self.Entry_2theta.config(fg=Defs.c_error_text)

    def good_2theta_input(self):
        self.Entry_2theta.config(fg=Defs.c_good_text)

    def get_Intensity_value(self):
        value = self.Entry_Intensity.get()

        try:
            self.intensity_value = float(value)
            self.good_intensity_input()
        except ValueError:
            self.bad_intensity_input()

        return self.intensity_value

    def bad_intensity_input(self):
        self.Entry_Intensity.config(fg=Defs.c_error_text)

    def good_intensity_input(self):
        self.Entry_Intensity.config(fg=Defs.c_good_text)

    def hide(self):
        self.widget_frame.grid_forget()

