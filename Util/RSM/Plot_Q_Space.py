import tkinter as tk
import matplotlib.pyplot as plt
import math

import Util.Definitions as Defs



class Plot_Q_Space:

    def __init__(self):

        self.fig_plot_Q_space_HfN = None  # Plotting Q-space with ewald sphere stuff!
        self.ax_plot_Q_space_HfN = None  # Plotting Q-space with ewald sphere stuff!

        self.wavelength = 1.5406 # Å

        self.Radius_Max = 4 * math.pi / self.wavelength
        self.Radius_small = 2 * math.pi / self.wavelength
        self.P_Center_X, self.P_Center_Y = 0, 0
        self.P_Inc_X, self.P_Inc_Y = self.Radius_small, 0
        self.P_Exit_X, self.P_Exit_Y = -self.Radius_small, 0

        self.lattice_param_HfN = 4.5253 # Å
        self.lattice_param_MgO = 4.2112 # Å

    def on_close_fig_plot_Q_space(self, event):
        self.fig_plot_Q_space_HfN = None
        self.ax_plot_Q_space_HfN = None
    def Plot_Q_Space(self):

        if self.fig_plot_Q_space_HfN is None:
            self.fig_plot_Q_space_HfN, self.ax_plot_Q_space_HfN = plt.subplots(num=Defs.fig_RSM_Q_Space)
            self.fig_plot_Q_space_HfN.suptitle("Q-space", fontsize=16)
            self.fig_plot_Q_space_HfN.canvas.mpl_connect('close_event', self.on_close_fig_plot_Q_space)
        self.ax_plot_Q_space_HfN.cla()

        Max_Circle = plt.Circle((self.P_Center_X, self.P_Center_Y), self.Radius_Max, color='k', fill=False)
        Inc_Circle = plt.Circle((self.P_Inc_X, self.P_Inc_Y), self.Radius_small, color='0.8', fill=True)
        Exit_Circle = plt.Circle((self.P_Exit_X, self.P_Exit_Y), self.Radius_small, color='0.8', fill=True)

        self.ax_plot_Q_space_HfN.set_ylim((0, 9))
        self.ax_plot_Q_space_HfN.set_xlim((-9, 9))
        self.ax_plot_Q_space_HfN.set_aspect(1)
        self.ax_plot_Q_space_HfN.set_xlabel(r'$Q_{||}$ [010] ($\mathrm{\AA^{-1}}$)')
        self.ax_plot_Q_space_HfN.set_ylabel(r'$Q_{-|}$ [100] ($\mathrm{\AA^{-1}}$)')

        self.ax_plot_Q_space_HfN.add_patch(Max_Circle)
        self.ax_plot_Q_space_HfN.add_patch(Inc_Circle)
        self.ax_plot_Q_space_HfN.add_patch(Exit_Circle)

        miller_h_values = range(6)
        miller_k_values = range(-5, 6, 1)

        self.ax_plot_Q_space_HfN.plot(-8, 7.5, 'gs')
        self.ax_plot_Q_space_HfN.annotate("HfN", (-8, 7.5))
        self.ax_plot_Q_space_HfN.plot(-8, 8, 'bo')
        self.ax_plot_Q_space_HfN.annotate("MgO", (-8, 8))

        for ix_h in miller_h_values:

            for ix_k in miller_k_values:

                Scaling_factor_HfN = 2 * math.pi / self.lattice_param_HfN
                Scaling_factor_MgO = 2 * math.pi / self.lattice_param_MgO

                Coord_HfN_X = ix_k * Scaling_factor_HfN
                Coord_HfN_Y = ix_h * Scaling_factor_HfN
                Coord_MgO_X = ix_k * Scaling_factor_MgO
                Coord_MgO_Y = ix_h * Scaling_factor_MgO

                length_HfN = math.sqrt(Coord_HfN_X ** 2 + Coord_HfN_Y ** 2)
                length_MgO = math.sqrt(Coord_MgO_X ** 2 + Coord_MgO_Y ** 2)

                if length_HfN < self.Radius_Max:
                    if self.allowed_by_FCC_structure_factor(ix_h, ix_k, 0):
                        self.ax_plot_Q_space_HfN.plot(Coord_HfN_X, Coord_HfN_Y, 'gs')
                        self.ax_plot_Q_space_HfN.annotate(str(ix_h) + str(ix_k) + "0", (Coord_MgO_X, Coord_MgO_Y))

                if length_MgO < self.Radius_Max:
                    if self.allowed_by_FCC_structure_factor(ix_h, ix_k, 0):
                        self.ax_plot_Q_space_HfN.plot(Coord_MgO_X, Coord_MgO_Y, 'bo')

        plt.show()

    def allowed_by_FCC_structure_factor(self, h, k, l):

        if h % 2 == 0: # All even numbers?
            if k % 2 == 0:
                if l % 2 == 0:
                    # All even!
                    return True # All even :)
                else:
                    return False # l is odd
            else:
                return False # k is odd

        else: # All odd numbers?
            if k % 2 == 0:
                return False # k is even
            else:
                if l % 2 == 0:
                    return False # l is even
                else:
                    return True # All are odd! :)


    def plot_RSM_Area(self, om_center, om_range, om_nr_points, tth_center, tth_range, tth_nr_points):
        # make arrays of omega angles and 2th angles.
        om_array = self.make_array(om_center, om_range, om_nr_points)
        tth_array = self.make_array(tth_center, tth_range, tth_nr_points)

        for omega in om_array:  # Plot line for each omega.
            QX_array = []
            QY_array = []

            for tth in tth_array:  # Make arrays of coordinates for 1 line
                qx = self.angles2Q_X(omega, tth)
                qy = self.angles2Q_Y(omega, tth)
                QX_array.append(qx)
                QY_array.append(qy)

            # Do the actual plotting of the line
            self.ax_plot_Q_space_HfN.plot(QX_array, QY_array, 'k--')

        # plot top and bottom line
        QX_array_first = []
        QY_array_first = []
        QX_array_last = []
        QY_array_last = []
        tth_first = tth_array[0]  # first angle
        tth_last = tth_array[-1]  # Last angle
        for omega in om_array:  # Make arrays of coordinates for 1 line
            QX_array_first.append(self.angles2Q_X(omega, tth_first))
            QY_array_first.append(self.angles2Q_Y(omega, tth_first))
            QX_array_last.append(self.angles2Q_X(omega, tth_last))
            QY_array_last.append(self.angles2Q_Y(omega, tth_last))
        # Do the actual plotting of the line
        self.ax_plot_Q_space_HfN.plot(QX_array_first, QY_array_first, 'k--')
        self.ax_plot_Q_space_HfN.plot(QX_array_last, QY_array_last, 'k--')

        plt.show()

    def make_array(self, center, range_of_area, nr_pts):
        array = []
        point_distance  = range_of_area / (nr_pts - 1)
        first_point = center - (range_of_area / 2)

        for ix in range(nr_pts):
            array.append(first_point + (float(ix) * point_distance))

        return array

    def angles2Q_X(self, om, tt):
        wavelength = self.wavelength # Å
        om_rad = math.radians(om)
        theta_rad = math.radians(tt/2)

        return 4*math.pi / wavelength * math.sin(theta_rad) * math.sin(theta_rad - om_rad)

    def angles2Q_Y(self, om, tt):
        wavelength = self.wavelength # Å
        om_rad = math.radians(om)
        theta_rad = math.radians(tt/2)

        return 4*math.pi / wavelength * math.sin(theta_rad) * math.cos(theta_rad - om_rad)
