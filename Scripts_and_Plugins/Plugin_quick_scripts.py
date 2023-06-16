
import tkinter as tk

import matplotlib.pyplot as plt
import Util.Definitions as Defs
import hyperspy.api as hs
from Util.My_Float_Entry import My_Float_Entry

import numpy as np


Description = """This script is here for quick scripting using function.
Best used for testing new stuff.

"""

class Plugin_Quick_Script:

    def __init__(self, Script_frame):
        self.script_frame = Script_frame # shared with all scripts

        self.active = False
        self.savable_script = False

        # Private frames
        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)  # Master within this scope
        self.entry_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.entry_frame.grid(row=9, column=0)


        # Master label
        self.label = tk.Label(self.my_frame, text="Quick scripting...", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Master description text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        self.button = tk.Button(self.my_frame, text="Run script", command=self.callback_button)
        self.button.grid(row=4, column=0, sticky="NW")

        self.Entry_Temperature = My_Float_Entry(self.entry_frame, "Temperature [K]", 300, 2, 0)
        self.Entry_molar_mass = My_Float_Entry(self.entry_frame, "molar mass", 29, 3, 0)
        self.Entry_sticking_coeff = My_Float_Entry(self.entry_frame, "Sticking coeff", 1, 3, 1)

        self.R_molar_gas_constant = 8.314472  # J / mol / K : Pa m3 / mol / K
        self.k_B_Boltzmann_const  = 1.380650 * 10**-23  # J / K
        self.b_B_Boltzmann_cons_eV= 8.617342 * 10**-5  # eV / K
        self.N_A_Avogadros_number = 6.022142 * 10**23  # Molecules per mol


    def callback_button(self):
        # self.function_sputtering_angular_distribution()
        # self.function_print_mean_free_path()
        # self.function_calculate_monolayer_time()

        eds_map = hs.load("3.bcf")
        eds_map[0].plot()

        print(eds_map)


    def function_calculate_monolayer_time(self):
        temperature = self.Entry_Temperature.get_value()
        n_mono = 10**19  # 1/cm2
        molar_mass = self.Entry_molar_mass.get_value()
        sticking_coeff = self.Entry_sticking_coeff.get_value()

        magic_const = 3.18 * 10**-25

        pressure = [1.333*10**-2, 1.333*10**-3, 1.333*10**-4, 1.333*10**-5, 1.333*10**-6, 1.333*10**-7, 1.333*10**-8]  # Pa
        collision_rate = []
        monolayer_time = []

        for pres in pressure:
            mon_time = magic_const * n_mono * np.sqrt(molar_mass * temperature) / pres

            monolayer_time.append(mon_time)
            collision_rate.append(n_mono / mon_time)

        print("Pressure in Pa", pressure)
        print("Collision rate", collision_rate)
        print("Monolayer time", monolayer_time)

    def function_print_mean_free_path(self):
        print("Mean free paths")
        temperature = 300 # Kelvin
        k_B = 1.38065 * 10**-23 # Joule/Kelvin = N*m/K
        diameter_Ar = 3.4 * 10**-10 # meter
        diameter_N2 = 3.64 * 10 ** -10 # meter
        print("Temp=", temperature, "Gas is N2")

        pressure_Torr_High = [0.001, 0.002, 0.003, 0.0045, 0.006, 0.0075, 0.010, 0.015, 0.020]
        pressure_Pa_High = [value * 133.322 for value in pressure_Torr_High] # Newton/meter2

        pressure_Torr_Low = [1 * 10**-4, 1 * 10**-5, 1 * 10**-6, 1 * 10**-7, 1 * 10**-8, 1 * 10**-9, 1 * 10**-10]
        pressure_Pa_Low = [value * 133.322 for value in pressure_Torr_Low] # Newton/meter2

        mean_free_path_high = []
        for pressure in pressure_Pa_High:
            temp_val = k_B * temperature / (np.sqrt(2) * np.pi * diameter_N2 * diameter_N2 * pressure)
            mean_free_path_high.append(temp_val)

        mean_free_path_low = []
        for pressure in pressure_Pa_Low:
            temp_val = k_B * temperature / (np.sqrt(2) * np.pi * diameter_N2 * diameter_N2 * pressure)
            mean_free_path_low.append(temp_val)

        print("Sputtering vacuum")
        for index in range(len(pressure_Torr_High)):
            print("Torr: ", pressure_Torr_High[index], "Pa: ", pressure_Pa_High[index], "lambda: ", mean_free_path_high[index])

        print("Background vacuum")
        for index in range(len(pressure_Torr_Low)):
            print("Torr: ", pressure_Torr_Low[index], "Pa: ", pressure_Pa_Low[index], "lambda: ",
                  mean_free_path_low[index])

    def function_sputtering_angular_distribution(self):
        print("function running")
        theta = np.arange(-np.pi/2, np.pi/2, 0.01)
        Ang_distr_cosine = self.Yield(theta, 0)
        Ang_distr_undercosine = self.Yield(theta, -0.5)
        Ang_distr_overcosine = self.Yield(theta, 0.5)
        Ang_distr_heart = self.Yield(theta, -0.8)

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        ax.plot(theta, Ang_distr_cosine)
        ax.plot(theta, Ang_distr_overcosine)
        ax.plot(theta, Ang_distr_undercosine)
        ax.plot(theta, Ang_distr_heart)

        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_thetalim(-np.pi/2, np.pi/2)
        ax.set_yticklabels([])
        ax.set_rmax(1.7)
        ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
        ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        ax.grid(True)

        plt.show()



    def Yield(self, thetas, fitting_param):
        cos_theta = np.cos(thetas)
        yield_of_theta = cos_theta * (1 + fitting_param * cos_theta * cos_theta)
        return yield_of_theta




    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()