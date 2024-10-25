import tkinter as tk

from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
from Util.Color_Scheme_Selector import Color_Scheme_Selector
from Util.My_Toggle_Switch import My_Toggle_Switch

import tkscrolledframe as SF
import Util.Definitions as Defs
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.colors import LogNorm
import scipy

import math

import numpy as np
import xrayutilities as xu

Description = """Plotting and analyzing RSMs

Interactive plots by pressing the figure buttons.
Origin  - Line to origin,  
Perpendicular - Perpendicular line through point
 
Center - Through-point for integration line
Vector - Direction of integration line

"""

class Plugin_RSM:

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

        self.fit_rsm_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.fit_rsm_frame.grid(row=7, column=0)

        self.test_button_frame = tk.Frame(self.my_frame, bg=Defs.c_script_entries)
        self.test_button_frame.grid(row=10, column=0)

        # Master label
        self.label = tk.Label(self.my_frame, text="Reciprocal Space Maps", bg=Defs.c_script_name)
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
        self.l_rsm_plotting = tk.Label(self.plot_rsm_frame, text="Plotting RSMs", bg=Defs.c_script_name)
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

        self.b_deconvolute_faults = tk.Button(self.plot_rsm_frame, text="Deconvolute", command=self.Callback_Deconvolute_Faults)
        self.b_deconvolute_faults.config(width=12)
        self.b_deconvolute_faults.grid(row=3, column=0, sticky="NW")

        self.e_lateral_point_qx = My_Float_Entry(self.plot_rsm_frame, "Lateral Q_x", -1.968, 3, 1)
        self.e_lateral_point_qx.set_entry_width(6)
        self.e_lateral_point_qy = My_Float_Entry(self.plot_rsm_frame, "Lateral Q_y", 4.17, 3, 2)
        self.e_lateral_point_qy.set_entry_width(7)
        self.e_tilt_point_qx = My_Float_Entry(self.plot_rsm_frame, "Tilt Q_x", -1.968, 4, 1)
        self.e_tilt_point_qx.set_entry_width(8)
        self.e_tilt_point_qy = My_Float_Entry(self.plot_rsm_frame, "Tilt Q_y", 4.17, 4, 2)
        self.e_tilt_point_qy.set_entry_width(8)

        # fit RSM stuff
        self.l_rsm_fitting = tk.Label(self.fit_rsm_frame, text="Fitting RSMs (Only first import file)", bg=Defs.c_script_name)
        self.l_rsm_fitting.grid(row=0, column=0, columnspan=10)
        self.l_rsm_fitting.config(font=('Helvetica', 11))

        self.b_plot_rsm_fitting = tk.Button(self.fit_rsm_frame, text="Plot fitting", command=self.callback_plot_rsm_fitting)
        self.b_plot_rsm_fitting.config(width=10)
        self.b_plot_rsm_fitting.grid(row=1, column=0, sticky="NW")
        self.Entry_aligned_omega = My_Float_Entry(self.fit_rsm_frame, "MgO(002) Om", 21.4545, 1, 1)
        self.Entry_aligned_2theta = My_Float_Entry(self.fit_rsm_frame, "MgO(002) 2th", 42.9091, 1, 2)

        self.Entry_GridX = My_Float_Entry(self.fit_rsm_frame, "Grid X", 200, 2, 0)
        self.Entry_GridY = My_Float_Entry(self.fit_rsm_frame, "Grid Y", 300, 2, 1)
        self.Entry_DynHigh = My_Float_Entry(self.fit_rsm_frame, "Dyn High", 0, 2, 2)
        self.Entry_DynLow = My_Float_Entry(self.fit_rsm_frame, "Dyn Low", 4.5, 2, 3)

        self.b_line_integration = tk.Button(self.fit_rsm_frame, text="Integration", command=self.callback_line_integration)
        self.b_line_integration.config(width=10)
        self.b_line_integration.grid(row=3, column=0, sticky="NW")
        self.Entry_no_of_pts_line = My_Float_Entry(self.fit_rsm_frame, "Pts in line", 100, 4, 1)
        self.Entry_line_cylinder_radius = My_Float_Entry(self.fit_rsm_frame, "Cyl radius", 0.02, 4, 2)
        self.Entry_thru_pt_X = My_Float_Entry(self.fit_rsm_frame, "Thru Pt X", -1.97, 5, 0)
        self.Entry_thru_pt_Y = My_Float_Entry(self.fit_rsm_frame, "Thru Pt Y", 4.17, 5, 1)
        self.Entry_vector_X = My_Float_Entry(self.fit_rsm_frame, "Vec X", 0.2, 5, 2)
        self.Entry_vector_Y = My_Float_Entry(self.fit_rsm_frame, "Vec Y", 0, 5, 3)

        self.integration_lin_log_index = 0
        self.b_int_linear = tk.Button(self.fit_rsm_frame, text="Linear", command=self.callback_int_lin_button)
        self.b_int_linear.grid(row=3, column=1, sticky="NW")
        self.b_int_log = tk.Button(self.fit_rsm_frame, text="Log", command=self.callback_int_log_button)
        self.b_int_log.grid(row=3, column=2, sticky="NW")
        self.callback_int_lin_button()

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

        # Plotting objects and settings
        self.fig_fit = None # Main fitting
        self.ax_fit = None # Main fitting
        self.center_int_pt_button = None
        self.ax_center_int_pt = None
        self.cid_select_center_int_pt = None
        self.vector_int_pt_button = None
        self.ax_vector_int_pt = None
        self.cid_select_vector_int_pt = None

        self.fig_fit_line_integration = None # Main line integration
        self.ax_fit_line_integration = None # Main line integration

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
        self.lateral_point_button = None  # For interactive rsm_q.
        self.ax_lateral = None  # For interactive rsm_q
        self.cid_select_lateral = None  # For interactive rsm_q
        self.tilt_point_button = None  # For interactive rsm_q.
        self.ax_tilt = None  # For interactive rsm_q
        self.cid_select_tilt = None  # For interactive rsm_q

        self.fig_plot_rsm_ang = None  # Main plotting angles
        self.ax_plot_rsm_ang = None  # Main plotting angles


    def on_close_fig_fitting(self, event):
        self.fig_fit = None
        self.ax_fit = None

    # Plotting the reciprocal space map, for fitting.
    # The data is put into a rectangular grid.
    def callback_plot_rsm_fitting(self):

        if self.fig_fit is None:
            self.fig_fit, self.ax_fit = plt.subplots(num=Defs.fig_RSM_fit)
            self.fig_fit.suptitle("Q-space, Gridded data", fontsize=16)
            self.fig_fit.canvas.mpl_connect('close_event', self.on_close_fig_fitting)
            self.ax_fit.set_aspect('equal')

            # Q-space figure buttons - For plotting lines
            self.ax_center_int_pt = self.fig_fit.add_axes([0.8, 0.9, 0.1, 0.075])
            self.center_int_pt_button = Button(self.ax_center_int_pt, "Center", color="lightblue", hovercolor="gold")
            self.center_int_pt_button.on_clicked(self.on_click_select_center_integration_point)

            self.ax_vector_int_pt = self.fig_fit.add_axes([0.7, 0.9, 0.1, 0.075])
            self.vector_int_pt_button = Button(self.ax_vector_int_pt, "Vector", color="lightblue", hovercolor="gold")
            self.vector_int_pt_button.on_clicked(self.on_click_select_vector_integ_pt)

        self.ax_fit.cla()

        MgO = xu.materials.MgO # Make a material

        om, tt, intensity = xu.io.getxrdml_map(self.file_paths[0]) # Get the angles from file

        hxrd = xu.HXRD(MgO.Q(1, 1, 0), MgO.Q(0, 0, 1)) # Create an experiment...

        [omnominal, _, _, ttnominal] = hxrd.Q2Ang(MgO.Q(0, 0, 2)) # Should use these to correct for offsets...
        omalign = self.Entry_aligned_omega.get_value()
        ttalign = self.Entry_aligned_2theta.get_value()
        # print("nominal omega: ", omnominal)
        # print("nominal 2theta: ", ttnominal)
        delta = [omalign - omnominal, ttalign - ttnominal]
        print("Delta om & tt: ", delta)

        qx, qy, qz = hxrd.Ang2Q(om, tt) # Convert angles to reciprocal space using offsets...

        # Create a regular grid
        gridder = xu.FuzzyGridder2D(int(self.Entry_GridX.get_value()), int(self.Entry_GridY.get_value()))
        # populate the grid with data.
        gridder(-qy, qz, intensity)

        INT = None
        if self.selection_index == 1: # log
            INT = xu.maplog(gridder.data.transpose(), self.Entry_DynLow.get_value(), self.Entry_DynHigh.get_value())
        elif self.selection_index == 2: # log2
            pass
        else:
            INT = gridder.data.transpose()

        cf = self.ax_fit.contour(gridder.xaxis, gridder.yaxis, INT, int(self.Entry_No_of_contours.get_value()), extend='min', cmap=self.color_selector.get_color())

        self.ax_fit.set_xlabel(r'$Q_{||}$ ($\mathrm{\AA^{-1}}$)')
        self.ax_fit.set_ylabel(r'$Q_{-|}$ ($\mathrm{\AA^{-1}}$)')

        plt.show()

    # interactive function
    def on_click_select_center_integration_point(self):
        self.cid_select_center_int_pt = self.fig_fit.canvas.mpl_connect('button_press_event',
                                                                        self.on_click_in_graph_center_integration)

    # interactive function
    def on_click_in_graph_center_integration(self, event):
        click_x, click_y = event.xdata, event.ydata
        self.Entry_thru_pt_X.set_entry_value(click_x)
        self.Entry_thru_pt_Y.set_entry_value(click_y)
        self.fig_fit.canvas.mpl_disconnect(self.cid_select_center_int_pt)

    # interactive function
    def on_click_select_vector_integ_pt(self, event):
        self.cid_select_vector_int_pt = self.fig_fit.canvas.mpl_connect('button_press_event',
                                                                        self.on_click_in_graph_vector_integration)

    # interactive function
    def on_click_in_graph_vector_integration(self, event):
        click_x, click_y = event.xdata, event.ydata

        center_point = np.array([self.Entry_thru_pt_X.get_value(), self.Entry_thru_pt_Y.get_value()])
        vector_point = np.array([click_x, click_y])

        vector = vector_point - center_point

        self.Entry_vector_X.set_entry_value(vector[0])
        self.Entry_vector_Y.set_entry_value(vector[1])
        self.fig_fit.canvas.mpl_disconnect(self.cid_select_vector_int_pt)

    def on_close_fig_line_int(self, event):
        self.fig_fit_line_integration = None
        self.ax_fit_line_integration = None

    # Integrate the map over a line (which is defined using point and vector)
    def callback_line_integration(self):

        if self.fig_fit_line_integration is None:
            self.fig_fit_line_integration, self.ax_fit_line_integration = plt.subplots(num=998)
            self.fig_fit_line_integration.suptitle("Line fitting graph", fontsize=16)
            self.fig_fit_line_integration.canvas.mpl_connect('close_event', self.on_close_fig_line_int)
        self.ax_fit_line_integration.cla()

        om, tt, intensity = xu.io.getxrdml_map(self.file_paths[0])  # Get the angles from file

        MgO = xu.materials.MgO  # Make a material
        hxrd = xu.HXRD(MgO.Q(1, 1, 0), MgO.Q(0, 0, 1))  # Create an experiment...

        [omnominal, _, _, ttnominal] = hxrd.Q2Ang(MgO.Q(0, 0, 2)) # Should use these for offset...
        omalign = self.Entry_aligned_omega.get_value()
        ttalign = self.Entry_aligned_2theta.get_value()
        #print("nominal omega: ", omnominal)
        #print("nominal 2theta: ", ttnominal)
        delta = [omalign - omnominal, ttalign - ttnominal]
        #print("Delta om & tt: ", delta)

        qx, qy, qz = hxrd.Ang2Q(om, tt, delta=delta)  # Convert angles to reciprocal space with offsets

        # integrate along qy (Q-space)
        line_point = np.array([self.Entry_thru_pt_X.get_value(), self.Entry_thru_pt_Y.get_value()]) # x, y
        line_vector = np.array([self.Entry_vector_X.get_value(), self.Entry_vector_Y.get_value()])  # x, y


        no_pts = int(self.Entry_no_of_pts_line.get_value())  # binning x-points
        int_radius = self.Entry_line_cylinder_radius.get_value()  # radius around the line to integrate

        # integration
        int_x, int_val, mask = xu.analysis.get_arbitrary_line([-qy, qz], intensity, line_point,
                                                              line_vector, npoints=no_pts, intrange=int_radius)

        # plot integrated data
        if self.integration_lin_log_index == 1:  # log
            self.ax_fit_line_integration.semilogy(int_x, int_val, 'bo-')
        else:
            self.ax_fit_line_integration.plot(int_x, int_val, 'bo-')


        # plot integration line in original plot where integration was done

        p0 = line_point
        p1 = line_point - 2 * line_vector # side-point for integration line
        p2 = line_point + 2 * line_vector # side-point for integration line
        p3 = line_point + line_vector     # vector click point

        self.ax_fit.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')
        self.ax_fit.plot(p0[0], p0[1], color='black', marker='*')
        self.ax_fit.plot(p3[0], p3[1], color='red', marker='^')

        # calculate the points for parallel lines to integration line which are integrated.
        vec_perp_cw =  [line_vector[1], -line_vector[0]] # clockwise perpendicular vector
        norm_factor = np.linalg.norm(vec_perp_cw)
        vec_perp_cw_normalized = np.array(vec_perp_cw) * (1/norm_factor)

        p5 = p1 + (int_radius * vec_perp_cw_normalized)
        p6 = p2 + (int_radius * vec_perp_cw_normalized)
        p7 = p1 - (int_radius * vec_perp_cw_normalized)
        p8 = p2 - (int_radius * vec_perp_cw_normalized)

        self.ax_fit.plot([p5[0], p6[0]], [p5[1], p6[1]], 'y--')
        self.ax_fit.plot([p7[0], p8[0]], [p7[1], p8[1]], 'y--')

        plt.show()


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


    # Add line to plot, perpendicular to origin line.
    def Callback_Deconvolute_Faults(self):
        #  Find intersecting point!
        #  Calculate the length of the vector from this point and the lateral point
        #  as well as the length of the vector from this point and the tilt point!
        #  Plot & print!
        k1 = self.horizontal_line_coefficients[0]
        m1 = self.horizontal_line_coefficients[1]
        k2 = self.tilt_line_coefficients[0]
        m2 = self.tilt_line_coefficients[1]

        # intersection point between horizontal and tilt lines
        qx_intersect = (m2-m1) / (k1-k2)
        qy_intersect = k1 * qx_intersect + m1
        self.intersect_point = [qx_intersect, qy_intersect]

        vec_hor_x = qx_intersect - self.e_lateral_point_qx.get_value()
        vec_hor_y = qy_intersect - self.e_lateral_point_qy.get_value()
        vec_tilt_x = qx_intersect - self.e_tilt_point_qx.get_value()
        vec_tilt_y = qy_intersect - self.e_tilt_point_qy.get_value()

        length_vec_hor = math.sqrt(vec_hor_x ** 2 + vec_hor_y ** 2)
        length_vec_tilt = math.sqrt(vec_tilt_x ** 2 + vec_tilt_y ** 2)

        print("Intersect point: ", self.intersect_point)
        print("Length of horizontal vector [/Å]: ", length_vec_hor)
        print("Length of tilt vector [/Å]: ", length_vec_tilt)

        # Avoid autoscaling of axis.
        current_xlim = self.ax_plot_rsm_q.get_xlim()
        current_ylim = self.ax_plot_rsm_q.get_ylim()

        self.ax_plot_rsm_q.plot([qx_intersect, self.e_lateral_point_qx.get_value()], [qy_intersect, self.e_lateral_point_qy.get_value()], 'gx-')
        self.ax_plot_rsm_q.plot([qx_intersect, self.e_tilt_point_qx.get_value()], [qy_intersect, self.e_tilt_point_qy.get_value()], 'gx-')

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

    # interactive function
    def on_click_select_lateral_point(self, event):
        self.cid_select_lateral = self.fig_plot_rsm_q.canvas.mpl_connect('button_press_event', self.on_click_in_graph_lateral_point)

    # interactive function
    def on_click_in_graph_lateral_point(self, event):
        click_x, click_y = event.xdata, event.ydata
        self.e_lateral_point_qx.set_entry_value(click_x)
        self.e_lateral_point_qy.set_entry_value(click_y)
        self.fig_plot_rsm_q.canvas.mpl_disconnect(self.cid_select_lateral)

        # Point which line should go through
        qx_l = click_x
        qy_l = click_y
        qx_l_right = qx_l + 0.2
        qx_l_left = qx_l - 0.2

        self.horizontal_line_coefficients[0] = 0  # k
        self.horizontal_line_coefficients[1] = qy_l  # m

        # Avoid autoscaling of axis.
        current_xlim = self.ax_plot_rsm_q.get_xlim()
        current_ylim = self.ax_plot_rsm_q.get_ylim()
        self.ax_plot_rsm_q.plot([qx_l_left, qx_l_right], [qy_l, qy_l], 'bo--')
        self.ax_plot_rsm_q.set_xlim(current_xlim)
        self.ax_plot_rsm_q.set_ylim(current_ylim)

        plt.show()


    # interactive function
    def on_click_select_tilt_point(self, event):
        self.cid_select_tilt = self.fig_plot_rsm_q.canvas.mpl_connect('button_press_event',self.on_click_in_graph_tilt_point)

    # interactive function
    def on_click_in_graph_tilt_point(self, event):
        click_x, click_y = event.xdata, event.ydata
        self.e_tilt_point_qx.set_entry_value(click_x)
        self.e_tilt_point_qy.set_entry_value(click_y)
        self.fig_plot_rsm_q.canvas.mpl_disconnect(self.cid_select_tilt)

        # Point which line should go through
        qx_p = click_x
        qy_p = click_y

        K_P = self.perpendicular_line_coefficients[0]
        M_P = qy_p - K_P * qx_p
        self.tilt_line_coefficients[0] = K_P  # k
        self.tilt_line_coefficients[1] = M_P  # m

        qy_p_below = qy_p - 0.2
        qx_p_below = (qy_p_below - M_P) / K_P
        qy_p_above = qy_p + 0.2
        qx_p_above = (qy_p_above - M_P) / K_P

        # Avoid autoscaling of axis when plotting.
        current_xlim = self.ax_plot_rsm_q.get_xlim()
        current_ylim = self.ax_plot_rsm_q.get_ylim()
        self.ax_plot_rsm_q.plot([qx_p_below, qx_p_above], [qy_p_below, qy_p_above], 'bo--')
        self.ax_plot_rsm_q.set_xlim(current_xlim)
        self.ax_plot_rsm_q.set_ylim(current_ylim)

        plt.show()



    # Plotting maps (multiple)
    def callback_plot_rsm(self):

        if self.fig_plot_rsm_q is None:
            self.fig_plot_rsm_q, self.ax_plot_rsm_q = plt.subplots(num=Defs.fig_RSM_q)
            self.fig_plot_rsm_q.suptitle("Q-space", fontsize=16)
            self.fig_plot_rsm_q.canvas.mpl_connect('close_event', self.on_close_fig_plot_rsm_q)
            self.ax_plot_rsm_q.set_aspect('equal')

            # Q-space figure buttons - For plotting lines
            self.ax_o_line = self.fig_plot_rsm_q.add_axes([0.8, 0.9, 0.1, 0.075])
            self.o_line_button = Button(self.ax_o_line, "Origin", color="lightblue", hovercolor="gold")
            self.o_line_button.on_clicked(self.on_click_select_o_line_point)

            self.ax_lateral = self.fig_plot_rsm_q.add_axes([0.7, 0.9, 0.1, 0.075])
            self.lateral_point_button = Button(self.ax_lateral, "Lateral", color="lightblue", hovercolor="gold")
            self.lateral_point_button.on_clicked(self.on_click_select_lateral_point)

            self.ax_tilt = self.fig_plot_rsm_q.add_axes([0.6, 0.9, 0.1, 0.075])
            self.tilt_point_button = Button(self.ax_tilt, "Tilt", color="lightblue", hovercolor="gold")
            self.tilt_point_button.on_clicked(self.on_click_select_tilt_point)

        if self.fig_plot_rsm_ang is None and self.toggle_plot_angles.is_on():
            self.fig_plot_rsm_ang, self.ax_plot_rsm_ang = plt.subplots(num=Defs.fig_RSM_w)
            self.fig_plot_rsm_ang.suptitle("2theta-omega", fontsize=16)
            self.fig_plot_rsm_ang.canvas.mpl_connect('close_event', self.on_close_fig_plot_rsm_ang)

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

    def callback_int_lin_button(self):
        self.integration_lin_log_index = 0
        self.b_int_log.config(bg=Defs.c_button_inactive)
        self.b_int_linear.config(bg=Defs.c_button_active)

    def callback_int_log_button(self):
        self.integration_lin_log_index = 1
        self.b_int_log.config(bg=Defs.c_button_active)
        self.b_int_linear.config(bg=Defs.c_button_inactive)

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