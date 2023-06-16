import tkinter as tk
import Util.Definitions as Defs
from Util.My_Float_Entry import My_Float_Entry
import matplotlib.pyplot as plt

import math as math
from pathlib import Path
import webbrowser as webbrowser


class calculate_angle_between_cubic_planes:

    def __init__(self, print_function, frame):

        self.print_function = print_function
        self.frame = frame

        self.label = tk.Label(self.frame, text="Calculate angle between planes, cubic lattice", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0, columnspan=10)
        self.label.config(font=('Helvetica', 11))

        self.b_calculate = tk.Button(self.frame, text="Calculate", command=self.callback_calculate)
        self.b_calculate.grid(row=1, column=0, sticky="NW")
        self.b_help_button = tk.Button(self.frame, text="How calc. is done", command=self.callback_help_button)
        self.b_help_button.grid(row=1, column=1, sticky="NW")
        self.b_crystal = tk.Button(self.frame, text="Generate Crystal", command=self.callback_crystal_button)
        self.b_crystal.grid(row=1, column=2, sticky="NW")

        self.entry_a_param = My_Float_Entry(self.frame, "Param a=b=c= ", 4.0, 2, 0)
        self.entry_a_param.set_entry_width(7)

        self.label_vec1 = tk.Label(self.frame, text="Vector1", bg=Defs.c_script_name)
        self.label_vec1.grid(row=3, column=0)
        self.label_vec1.config(font=('Helvetica', 11))
        self.lattice_vector_1_h = My_Float_Entry(self.frame, "h", 1, 3, 1)
        self.lattice_vector_1_k = My_Float_Entry(self.frame, "k", 0, 3, 2)
        self.lattice_vector_1_l = My_Float_Entry(self.frame, "l", 0, 3, 3)

        self.label_vec2 = tk.Label(self.frame, text="Vector2", bg=Defs.c_script_name)
        self.label_vec2.grid(row=4, column=0)
        self.label_vec2.config(font=('Helvetica', 11))
        self.lattice_vector_2_h = My_Float_Entry(self.frame, "h", 0, 4, 1)
        self.lattice_vector_2_k = My_Float_Entry(self.frame, "k", 0, 4, 2)
        self.lattice_vector_2_l = My_Float_Entry(self.frame, "l", 1, 4, 3)

        self.a = 1

        self.fig_cube_crystal = None
        self.ax_cube_crystal = None


    def callback_calculate(self):
        a = self.entry_a_param.get_value()

        h1 = self.lattice_vector_1_h.get_value()
        k1 = self.lattice_vector_1_k.get_value()
        l1 = self.lattice_vector_1_l.get_value()

        h2 = self.lattice_vector_2_h.get_value()
        k2 = self.lattice_vector_2_k.get_value()
        l2 = self.lattice_vector_2_l.get_value()

        numerator = h1*h2 + k1*k2 + l1*l2

        denom_p1 = math.sqrt(h1*h1 + k1*k1 + l1*l1)
        denom_p2 = math.sqrt(h2*h2 + k2*k2 + l2*l2)
        denominator = denom_p1 * denom_p2

        cos_theta = numerator / denominator
        theta = math.acos(cos_theta)
        self.print_function("Angle = " + str(math.degrees(theta)) + "\n")

    def callback_help_button(self):
        Script_Path = Path.cwd()
        rel_path1 = "Scripts_and_Plugins\Calculations_Scripts\Crystallographic_Interplanar_Angles.pdf"
        file_path1 = (Script_Path / rel_path1).resolve()
        webbrowser.open_new(file_path1)
        self.print_function("Using the equation provided by Han, Kang and Suh\n")


    def on_close_3D_fig(self, event):
        self.fig_hex_crystal = None
        self.ax_hex_crystal = None

    def callback_crystal_button(self):
        pass

        """
        if self.fig_hex_crystal is None:
            self.fig_hex_crystal = plt.figure(Defs.fig_lattice_hex)
            self.ax_hex_crystal = self.fig_hex_crystal.add_subplot(projection='3d')
            self.fig_hex_crystal.suptitle("Hexagonal Lattice ", fontsize=16)
            self.fig_hex_crystal.canvas.mpl_connect('close_event', self.on_close_3D_fig)

        x_points = self.x_points_hexagon + self.x_points_hexagon
        y_points = self.y_points_hexagon + self.y_points_hexagon
        z_points = self.z_points_hexagon + [z + self.c for z in self.z_points_hexagon]

        self.ax_hex_crystal.scatter(x_points, y_points, z_points, color="blue", s=100)

        for index in range(len(self.z_points_hexagon)):
            x_line = [x_points[index], x_points[index + len(self.z_points_hexagon)]]
            y_line = [y_points[index], y_points[index + len(self.z_points_hexagon)]]
            z_line = [z_points[index], z_points[index + len(self.z_points_hexagon)]]
            self.ax_hex_crystal.plot(x_line, y_line, z_line, 'gray')

        plt.show()
        """
