import tkinter as tk

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
from Util.My_Integer_Entry import My_Integer_Entry
from Util.Color_Scheme_Selector import Color_Scheme_Selector
from Util.My_Toggle_Switch import My_Toggle_Switch
from Util.RSM.Coordinate_Selector import Coordinate_Selector
from Util.RSM.Plot_Q_Space import Plot_Q_Space

import tkscrolledframe as SF
import Util.Definitions as Defs
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.colors import LogNorm
import scipy

import math

import numpy as np
import xrayutilities as xu

Description = """Plotting RSMs

Calculate areas in reciprocal space 
covered by the given angular ranges

"""

class Plugin_RSM_Planning:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler # to get data from

        self.active = False
        self.savable_script = False

        # Private frames
        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries)  # Master within this scope

        self.sframe = SF.ScrolledFrame(self.my_frame, width=400, height=160)
        self.sframe.grid(row=11, column=0, columnspan=3)
        self.sframe.config(bg=Defs.c_frame_color)
        self.sframe.bind_arrow_keys(self.my_frame)
        self.sframe.bind_scroll_wheel(self.my_frame)
        self.label_entry_frame = self.sframe.display_widget(tk.Frame)
        self.label_entry_frame.config(bg=Defs.c_frame_color)

        self.master_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.master_button_frame.grid(row=3, column=0)
        self.select_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.select_button_frame.grid(row=4, column=0)
        self.general_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.general_frame.grid(row=5, column=0)

        self.plot_rsm_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.plot_rsm_frame.grid(row=6, column=0)
        self.planning_rsm_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.planning_rsm_frame.grid(row=7, column=0)

        self.test_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.test_button_frame.grid(row=10, column=0)

        # Master label
        self.label = tk.Label(self.my_frame, text="Planning Reciprocal Space Maps", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Master description text
        self.text = tk.Text(self.my_frame, width=50, height=10, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')



        # Master Buttons
        self.b_import = tk.Button(self.master_button_frame, text="Import", command=self.callback_import_button)
        self.b_import.config(width=8)
        self.b_import.grid(row=0, column=0, sticky="NW")
        self.b_import_all = tk.Button(self.master_button_frame, text="Import All", command=self.callback_import_all_button)
        self.b_import_all.config(width=8)
        self.b_import_all.grid(row=0, column=1, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files", command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=2, sticky="NW")

        # Selection buttons
        self.selection_index = 1
        self.b_linear = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=5, column=0, sticky="NW")
        self.b_log = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=5, column=1, sticky="NW")
        self.b_lin_half_int = tk.Button(self.select_button_frame, text="Lin halving countors", command=self.callback_lin_half_int_button)
        self.b_lin_half_int.grid(row=5, column=2, sticky="NW")

        # General stuff
        self.l_rsm_general = tk.Label(self.general_frame, text="General settings", bg=Defs.c_script_name)
        self.l_rsm_general.grid(row=0, column=0, columnspan=10)
        self.l_rsm_general.config(font=('Helvetica', 11))
        self.color_selector = Color_Scheme_Selector(self.general_frame, 'jet', 1, 0)
        self.Entry_No_of_contours = My_Float_Entry(self.general_frame, "# Contours", 8, 1, 1)

        # Plot RSM stuff
        self.l_rsm_plotting = tk.Label(self.plot_rsm_frame, text="Plotting actual RSM data", bg=Defs.c_script_name)
        self.l_rsm_plotting.grid(row=0, column=0, columnspan=10)
        self.l_rsm_plotting.config(font=('Helvetica', 11))
        self.b_plot_rsm = tk.Button(self.plot_rsm_frame, text="Plot RSM", command=self.callback_plot_rsm)
        self.b_plot_rsm.config(width=8)
        self.b_plot_rsm.grid(row=1, column=0, sticky="NW")
        self.e_rsm_min_int_for_log = My_Float_Entry(self.plot_rsm_frame, "Min int", 0.4, 1, 1)
        self.e_reduced_max_intensity = My_Float_Entry(self.plot_rsm_frame, "Reduce max by x", 100, 1, 2)
        self.toggle_plot_angles = My_Toggle_Switch(self.plot_rsm_frame, "Plot angles", 1, 3)

        self.b_add_line_to_origin = tk.Button(self.plot_rsm_frame, text="Line to origin", command=self.callback_line_to_origin_and_perp)
        self.b_add_line_to_origin.config(width=12)
        self.b_add_line_to_origin.grid(row=2, column=0, sticky="NW")
        self.e_line_to_origin_qx = My_Float_Entry(self.plot_rsm_frame, "Q_x", -2.1092, 2, 1)
        self.e_line_to_origin_qx.set_entry_width(8)
        self.e_line_to_origin_qy = My_Float_Entry(self.plot_rsm_frame, "Q_y", 4.4766, 2, 2)
        self.e_line_to_origin_qy.set_entry_width(8)

        self.b_toggle_use_plot_limits = My_Toggle_Switch(self.plot_rsm_frame, "Apply plot limits", 4, 0)
        self.e_xlim_min = My_Float_Entry(self.plot_rsm_frame, "X-lim min", -3.3, 4, 1)
        self.e_xlim_max = My_Float_Entry(self.plot_rsm_frame, "X-lim max", -2.1, 4, 2)
        self.e_ylim_min = My_Float_Entry(self.plot_rsm_frame, "Y-lim min", 4.8, 5, 1)
        self.e_ylim_max = My_Float_Entry(self.plot_rsm_frame, "Y-lim max", 6.2, 5, 2)


        # Planning RSM stuff
        self.l_rsm_planning = tk.Label(self.planning_rsm_frame, text="Planning RSM measurements", bg=Defs.c_script_name)
        self.l_rsm_planning.grid(row=0, column=0, columnspan=10)
        self.l_rsm_planning.config(font=('Helvetica', 11))
            # Extra frame to house buttons...
        self.planning_rsm_buttons_frame = tk.Frame(self.planning_rsm_frame, bg=Defs.c_script_entries)
        self.planning_rsm_buttons_frame.grid(row=1, column=0, columnspan=10)
        self.b_set_selected_point = tk.Button(self.planning_rsm_buttons_frame, text="Set selection", command=self.callback_set_selection)
        self.b_set_selected_point.config(width=10)
        self.b_set_selected_point.grid(row=0, column=0, sticky="NW")
        self.point_selector = Coordinate_Selector(self.planning_rsm_buttons_frame, "MgO 200", 0, 1)
            # For plotting Q-space with Ewald Sphere
        self.b_plot_Q_space =  tk.Button(self.planning_rsm_buttons_frame, text="Plot Q-space", command=self.callback_plot_Q_space)
        self.b_plot_Q_space.config(width=10)
        self.b_plot_Q_space.grid(row=0, column=3, sticky="NW")
        self.o_Q_space_plotter = Plot_Q_Space()
        self.b_plot_area_in_Q_space = tk.Button(self.planning_rsm_buttons_frame, text="Area in Q-space", command=self.callback_plot_Area_in_Q_space)
        self.b_plot_area_in_Q_space.config(width=12)
        self.b_plot_area_in_Q_space.grid(row=0, column=4, sticky="NW")


        self.b_plot_area_from_angles = tk.Button(self.planning_rsm_frame, text="Plot RSM area", command=self.callback_plot_RSM_Area)
        self.b_plot_area_from_angles.config(width=12)
        self.b_plot_area_from_angles.grid(row=6, column=0, sticky="NW")
        self.b_plot_area_from_angles = tk.Button(self.planning_rsm_frame, text="Plot RSM point", command=self.callback_plot_RSM_Point)
        self.b_plot_area_from_angles.config(width=12)
        self.b_plot_area_from_angles.grid(row=7, column=0, sticky="NW")

        self.e_omega_center_point = My_Float_Entry(self.planning_rsm_frame, "w center", 21.4589, 6, 1)
        self.e_omega_center_point.set_entry_width(8)
        self.e_omega_range = My_Float_Entry(self.planning_rsm_frame, "w range", 5, 6, 2)
        self.e_omega_nr_points = My_Integer_Entry(self.planning_rsm_frame, "w nr. pts", 10, 6, 3)

        self.e_2th_center_point = My_Float_Entry(self.planning_rsm_frame, "2th center", 42.9178, 7, 1)
        self.e_2th_center_point.set_entry_width(8)
        self.e_2th_range = My_Float_Entry(self.planning_rsm_frame, "2th range", 5, 7, 2)
        self.e_2th_nr_points = My_Integer_Entry(self.planning_rsm_frame, "w nr. pts", 10, 7, 3)


        # Test Buttons
        self.b_test3 = tk.Button(self.test_button_frame, text="Test3", command=self.callback_test3)
        self.b_test3.config(width=8)
        self.b_test3.grid(row=0, column=2, sticky="NW")


        self.callback_log_button()
        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.file_paths = []
        self.data_labels = []


        ## Stuff connected to main plotting and calculations.
        self.origin_line_coefficients = [0, 0]
        self.perpendicular_line_coefficients = [0, 0]
        self.horizontal_line_coefficients = [0, 0]
        self.tilt_line_coefficients = [0, 0]
        self.intersect_point = [0, 0]
        self.fig_plot_rsm_q = None  # Main plotting
        self.ax_plot_rsm_q = None # Main plotting
        self.o_line_button = None # For interactive rsm_q Point through origin line is drawn
        self.ax_o_line = None # For interactive rsm_q
        self.cid_select_o_line = None # For interactive rsm_q

        self.fig_plot_rsm_ang = None  # Main plotting angles
        self.ax_plot_rsm_ang = None  # Main plotting angles



    def init_figures_for_plotting(self):
        if self.fig_plot_rsm_q is None:
            self.fig_plot_rsm_q, self.ax_plot_rsm_q = plt.subplots(num=Defs.fig_RSM_plan)
            self.fig_plot_rsm_q.suptitle("Q-space", fontsize=16)
            self.fig_plot_rsm_q.canvas.mpl_connect('close_event', self.on_close_fig_plot_rsm_q)
            self.ax_plot_rsm_q.set_aspect('equal')

            # Q-space figure buttons - For plotting lines
            self.ax_o_line = self.fig_plot_rsm_q.add_axes([0.8, 0.9, 0.1, 0.075])
            self.o_line_button = Button(self.ax_o_line, "Origin", color="lightblue", hovercolor="gold")
            self.o_line_button.on_clicked(self.on_click_select_o_line_point)

        if self.fig_plot_rsm_ang is None and self.toggle_plot_angles.is_on():
            self.fig_plot_rsm_ang, self.ax_plot_rsm_ang = plt.subplots(num=Defs.fig_RSM_plan_w)
            self.fig_plot_rsm_ang.suptitle("2theta-omega", fontsize=16)
            self.fig_plot_rsm_ang.canvas.mpl_connect('close_event', self.on_close_fig_plot_rsm_ang)

    def callback_plot_RSM_Point(self):
        self.init_figures_for_plotting()
        om_center = self.e_omega_center_point.get_value()
        tth_center = self.e_2th_center_point.get_value()
        QX = self.angles2Q_X(om_center, tth_center)
        QY = self.angles2Q_Y(om_center, tth_center)

        self.ax_plot_rsm_q.plot(QX, QY, 'r*')

        # set the axis labels and show plot
        self.ax_plot_rsm_q.set_xlabel(r'$Q_{||}$ ($\mathrm{\AA^{-1}}$)')
        self.ax_plot_rsm_q.set_ylabel(r'$Q_{-|}$ ($\mathrm{\AA^{-1}}$)')

        if self.toggle_plot_angles.is_on():
            self.ax_plot_rsm_ang.set_xlabel(r"$2\mathrm{\theta \ (^o)} $ ")
            self.ax_plot_rsm_ang.set_ylabel(r"$\mathrm{\omega \ (^o)} $ ")

        plt.show()

    def callback_plot_RSM_Area(self):

        self.init_figures_for_plotting()

        om_center = self.e_omega_center_point.get_value()
        om_range = self.e_omega_range.get_value()
        om_nr_points = int(self.e_omega_nr_points.get_value())
        tth_center = self.e_2th_center_point.get_value()
        tth_range = self.e_2th_range.get_value()
        tth_nr_points = int(self.e_2th_nr_points.get_value())

        # make arrays of omega angles and 2th angles.
        om_array = self.make_array(om_center, om_range, om_nr_points)
        tth_array = self.make_array(tth_center, tth_range, tth_nr_points)

        for omega in om_array : # Plot line for each omega.
            QX_array = []
            QY_array = []

            for tth in tth_array: # Make arrays of coordinates for 1 line
                qx = self.angles2Q_X(omega, tth)
                qy = self.angles2Q_Y(omega, tth)
                QX_array.append(qx)
                QY_array.append(qy)

            # Do the actual plotting of the line
            self.ax_plot_rsm_q.plot(QX_array, QY_array, 'k--')

        # plot top and bottom line
        QX_array_first = []
        QY_array_first = []
        QX_array_last = []
        QY_array_last = []
        tth_first = tth_array[0] # first angle
        tth_last = tth_array[-1]  # Last angle
        for omega in om_array:  # Make arrays of coordinates for 1 line
            QX_array_first.append(self.angles2Q_X(omega, tth_first))
            QY_array_first.append(self.angles2Q_Y(omega, tth_first))
            QX_array_last.append(self.angles2Q_X(omega, tth_last))
            QY_array_last.append(self.angles2Q_Y(omega, tth_last))
        # Do the actual plotting of the line
        self.ax_plot_rsm_q.plot(QX_array_first, QY_array_first, 'k--')
        self.ax_plot_rsm_q.plot(QX_array_last, QY_array_last, 'k--')

        # set the axis labels and show plot
        self.ax_plot_rsm_q.set_xlabel(r'$Q_{||}$ ($\mathrm{\AA^{-1}}$)')
        self.ax_plot_rsm_q.set_ylabel(r'$Q_{-|}$ ($\mathrm{\AA^{-1}}$)')

        if self.toggle_plot_angles.is_on():
            self.ax_plot_rsm_ang.set_xlabel(r"$2\mathrm{\theta \ (^o)} $ ")
            self.ax_plot_rsm_ang.set_ylabel(r"$\mathrm{\omega \ (^o)} $ ")

        plt.show()

    def make_array(self, center, range_of_area, nr_pts):
        array = []
        point_distance  = range_of_area / (nr_pts - 1)
        first_point = center - (range_of_area / 2)

        for ix in range(nr_pts):
            array.append(first_point + (float(ix) * point_distance))

        return array





    def on_close_fig_plot_rsm_q(self, event):
        self.fig_plot_rsm_q = None
        self.ax_plot_rsm_q = None

    def on_close_fig_plot_rsm_ang(self, event):
        self.fig_plot_rsm_ang = None
        self.ax_plot_rsm_ang = None

    # Add line from origin through point
    def callback_line_to_origin_and_perp(self):
        # Point which Origin-line should go through
        qx_o = self.e_line_to_origin_qx.get_value()
        qy_o = self.e_line_to_origin_qy.get_value()
        coeff_line = qy_o / qx_o # Linear equation coefficient
        self.origin_line_coefficients[0] = coeff_line # k
        self.origin_line_coefficients[1] = 0 # m
        #Calculate position beyond the given so line goes through the point
        qy_above = qy_o + 0.2
        qx_above = qy_above / coeff_line

        # Perpendicular line through the same point.
        K_P = -1 / coeff_line  # Linear equation coefficient for perpendicular line
        M_P = qy_o - K_P * qx_o  # Linear equation intercept for perpendicular line
        self.perpendicular_line_coefficients[0] = K_P  # k
        self.perpendicular_line_coefficients[1] = M_P  # m
        # Points to plot through
        qy_p_below = qy_o - 0.2
        qx_p_below = (qy_p_below - M_P) / K_P
        qy_p_above = qy_o + 0.2
        qx_p_above = (qy_p_above - M_P) / K_P

        # Avoid autoscaling of axis.
        current_xlim = self.ax_plot_rsm_q.get_xlim()
        current_ylim = self.ax_plot_rsm_q.get_ylim()

        self.ax_plot_rsm_q.plot([0, qx_above], [0, qy_above], 'ko:')
        self.ax_plot_rsm_q.plot([qx_p_below, qx_p_above], [qy_p_below, qy_p_above], 'ko:')

        self.ax_plot_rsm_q.set_xlim(current_xlim)
        self.ax_plot_rsm_q.set_ylim(current_ylim)

        plt.show()


    #interactive function
    def on_click_select_o_line_point(self, event):
        self.cid_select_o_line = self.fig_plot_rsm_q.canvas.mpl_connect('button_press_event', self.on_click_in_graph_o_line)

    # interactive function
    def on_click_in_graph_o_line(self, event):
        click_x, click_y = event.xdata, event.ydata
        self.e_line_to_origin_qx.set_entry_value(click_x)
        self.e_line_to_origin_qy.set_entry_value(click_y)
        self.fig_plot_rsm_q.canvas.mpl_disconnect(self.cid_select_o_line)

        self.callback_line_to_origin_and_perp() # Plot the line.


    # Plotting maps (multiple)
    def callback_plot_rsm(self):

        self.init_figures_for_plotting()
        self.ax_plot_rsm_q.cla()
        if self.toggle_plot_angles.is_on():
            self.ax_plot_rsm_ang.cla()


        for path_ in self.file_paths:

            # Get values, omega, 2theta and intensity
            xf_map_scan = xu.io.XRDMLFile(path_)
            tt = xf_map_scan.scan['2Theta']
            om = xf_map_scan.scan['Omega']
            int_raw =  xf_map_scan.scan['detector']
            int_fixed = np.where(int_raw<self.e_rsm_min_int_for_log.get_value(), 0, int_raw)

            # Format to the same shape
            tt_, om_ = np.meshgrid(tt[0], om)

            QX = np.zeros(tt_.shape)
            QY = np.zeros(tt_.shape)

            size_om = QX.shape[0]
            size_tt = QX.shape[1]

            for ix_om in range(size_om) :
                for ix_tt in range(size_tt) :
                    QX[ix_om][ix_tt] = self.angles2Q_X(om_[ix_om][ix_tt], tt_[ix_om][ix_tt])
                    QY[ix_om][ix_tt] = self.angles2Q_Y(om_[ix_om][ix_tt], tt_[ix_om][ix_tt])


            if self.selection_index == 0 : # linear
                cf = self.ax_plot_rsm_q.contour(QX, QY, int_fixed, int(self.Entry_No_of_contours.get_value()), extend='min', cmap=self.color_selector.get_color())
                if self.toggle_plot_angles.is_on():
                    cf = self.ax_plot_rsm_ang.contour(tt_, om_, int_fixed, int(self.Entry_No_of_contours.get_value()), extend='min', cmap=self.color_selector.get_color())
            elif self.selection_index == 2:  # Plot linear with levels at halving intensities.

                Number_of_contours = int(self.Entry_No_of_contours.get_value())
                Max_intensity = np.max(int_fixed)
                Almost_max_intensity = Max_intensity - self.e_reduced_max_intensity.get_value()

                contour_levels = []
                for ix in reversed(range(1, Number_of_contours)): # Reverse the list. Divide with big number first...
                    contour_levels.append(Max_intensity / (2**ix))
                contour_levels.append(Almost_max_intensity)

                print("Max intensity: ", Max_intensity)
                print("Contour levels: ", contour_levels)
                cf = self.ax_plot_rsm_q.contour(QX, QY, int_fixed, contour_levels, extend='min', cmap=self.color_selector.get_color())
                if self.toggle_plot_angles.is_on():
                    cf = self.ax_plot_rsm_ang.contour(tt_, om_, int_fixed, contour_levels, extend='min', cmap=self.color_selector.get_color())

            else: # Log10
                cf = self.ax_plot_rsm_q.contour(QX, QY, np.log10(int_fixed), int(self.Entry_No_of_contours.get_value()), extend='min', cmap=self.color_selector.get_color())
                if self.toggle_plot_angles.is_on():
                    cf = self.ax_plot_rsm_ang.contour(tt_, om_, np.log10(int_fixed), int(self.Entry_No_of_contours.get_value()), extend='min', cmap=self.color_selector.get_color())

        self.ax_plot_rsm_q.set_xlabel(r'$Q_{||}$ ($\mathrm{\AA^{-1}}$)')
        self.ax_plot_rsm_q.set_ylabel(r'$Q_{-|}$ ($\mathrm{\AA^{-1}}$)')

        if self.b_toggle_use_plot_limits.is_on():
            self.ax_plot_rsm_q.set_xlim(self.e_xlim_min.get_value(), self.e_xlim_max.get_value())
            self.ax_plot_rsm_q.set_ylim(self.e_ylim_min.get_value(), self.e_ylim_max.get_value())

        if self.toggle_plot_angles.is_on():
            self.ax_plot_rsm_ang.set_xlabel(r"$2\mathrm{\theta \ (^o)} $ ")
            self.ax_plot_rsm_ang.set_ylabel(r"$\mathrm{\omega \ (^o)} $ ")

        plt.show()


    def angles2Q_X(self, om, tt):
        wavelength = 1.5406 # Å
        om_rad = math.radians(om)
        theta_rad = math.radians(tt/2)

        return 4*math.pi / wavelength * math.sin(theta_rad) * math.sin(theta_rad - om_rad)

    def angles2Q_Y(self, om, tt):
        wavelength = 1.5406 # Å
        om_rad = math.radians(om)
        theta_rad = math.radians(tt/2)

        return 4*math.pi / wavelength * math.sin(theta_rad) * math.cos(theta_rad - om_rad)

    def callback_test3(self):
        pass

    def callback_plot_Q_space(self):
        self.o_Q_space_plotter.Plot_Q_Space()

    def callback_plot_Area_in_Q_space(self):
        om_center = self.e_omega_center_point.get_value()
        om_range = self.e_omega_range.get_value()
        om_nr_pts = self.e_omega_nr_points.get_value()
        tth_center = self.e_2th_center_point.get_value()
        tth_range = self.e_2th_range.get_value()
        tth_nr_pts = self.e_2th_nr_points.get_value()

        self.o_Q_space_plotter.plot_RSM_Area(om_center, om_range, om_nr_pts, tth_center, tth_range, tth_nr_pts)


    def callback_set_selection(self):
        coords = self.point_selector.get_selected_coordinates()
        self.e_omega_center_point.set_entry_value(coords[0])
        self.e_2th_center_point.set_entry_value(coords[1])

    def callback_linear_button(self):
        self.selection_index = 0
        self.unmark_select_buttons()
        self.b_linear.config(bg=Defs.c_button_active)

    def callback_log_button(self):
        self.selection_index = 1
        self.unmark_select_buttons()
        self.b_log.config(bg=Defs.c_button_active)

    def callback_lin_half_int_button(self):
        self.selection_index = 2
        self.unmark_select_buttons()
        self.b_lin_half_int.config(bg=Defs.c_button_active)

    def unmark_select_buttons(self):
        self.b_linear.config(bg=Defs.c_button_inactive)
        self.b_log.config(bg=Defs.c_button_inactive)
        self.b_lin_half_int.config(bg=Defs.c_button_inactive)

    def callback_import_all_button(self):

        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1

            file_path = data_in_file.get_path()
            file_name = data_in_file.get_name()

            self.file_paths.append(file_path)

            new_entry = My_Label_Entry(self.label_entry_frame, file_name, self.no_files_index, 0)
            new_entry.set_label_bg("seagreen1")
            new_entry.set_entry_value(data_in_file.file_name)
            self.data_labels.append(new_entry)

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()

        file_path = data.get_path()
        file_name = data.get_name()

        self.file_paths.append(file_path)

        new_entry = My_Label_Entry(self.label_entry_frame, file_name, self.no_files_index, 0)
        new_entry.set_entry_value(file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels :
            label_.hide()
        self.file_data[:] = []
        self.file_paths[:] = []
        self.data_labels[:] = []


    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()