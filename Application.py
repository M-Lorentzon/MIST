from File_Handler import *
from Text_Plotter import *
from Scripts_and_Plugins.Plugin_MOS import *
from Scripts_and_Plugins.Plugin_XRD1 import *
from Scripts_and_Plugins.Plot_Stacked_Graphs import *
from Scripts_and_Plugins.Plugin_Pole_fig import *

class Application:
    def __init__(self, window):
        self.window = window
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        # Main frames
        self.frame_info = tk.Frame(self.window, bg=Defs.c_frame_color)
        self.frame_info.grid(column=0, row=0, sticky="NSEW")
        self.frame_scripts = tk.Frame(self.window, bg=Defs.c_frame_color)
        self.frame_scripts.grid(column=1, row=0, sticky="NSEW")
        self.frame_view = tk.Frame(self.window, bg=Defs.c_frame_color, width=400, height=100)
        self.frame_view.grid(column=2, row=0, sticky="NSEW")

        # frames in Info frame
        self.frame_info_global_buttons = tk.Frame(self.frame_info, bg=Defs.c_frame_color)
        self.frame_info_global_buttons.grid(column=0, row=1, sticky="NSEW", padx=20, pady=5)
        self.frame_info_script_buttons = tk.Frame(self.frame_info, bg=Defs.c_frame_color)
        self.frame_info_script_buttons.grid(column=0, row=2, sticky="NSEW", padx=20, pady=5)
        self.frame_info_file_handler = tk.Frame(self.frame_info, bg=Defs.c_frame_color)
        self.frame_info_file_handler.grid(column=0, row=3, sticky="NSEW", padx=20, pady=5)

        # Global buttons
        self.b_open = tk.Button(self.frame_info_global_buttons, text="Open file ", command=self.open_file)
        self.b_open.grid(row=0, column=0, sticky="NW")
        self.b_close = tk.Button(self.frame_info_global_buttons, text="Save file ", command=self.save_file)
        self.b_close.grid(row=0, column=1, sticky="NW")
        self.b_remove_files = tk.Button(self.frame_info_global_buttons, text="Clear files ", command=self.remove_files)
        self.b_remove_files.grid(row=2, column=0, sticky="NW")

        # Script selection buttons
        self.b_select_mos = tk.Button(self.frame_info_script_buttons, text="MOS", command=self.callback_mos_button)
        self.b_select_mos.config(width=8)
        self.b_select_mos.grid(row=0, column=0, sticky="NW")
        self.b_select_xrd1 = tk.Button(self.frame_info_script_buttons, text="XRD1", command=self.callback_xrd1_button)
        self.b_select_xrd1.config(width=8)
        self.b_select_xrd1.grid(row=0, column=1, sticky="NW")
        self.b_select_xrd_plot = tk.Button(self.frame_info_script_buttons, text="Plot_XRD", command=self.callback_plot_xrd_button)
        self.b_select_xrd_plot.config(width=8)
        self.b_select_xrd_plot.grid(row=2, column=0, sticky="NW")
        self.b_select_pole_fig = tk.Button(self.frame_info_script_buttons, text="Pole-fig",command=self.callback_pole_fig_button)
        self.b_select_pole_fig.config(width=8)
        self.b_select_pole_fig.grid(row=2, column=1, sticky="NW")

        # Labels
        self.text_intro = tk.Label(self.frame_info, text=Defs.t_intro, bg=Defs.c_description_color)
        self.text_intro.grid(row=0, sticky="WE", columnspan=10)

        # Actual objects to do work!
        self.o_file_handler = file_handler(self.frame_info_file_handler)
        self.o_Text_Plotter = Text_Plotter(self.frame_view)
        self.o_MOS_script = MOS_Script(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
        self.o_XRD1_script = Plugin_XRD1(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
        self.o_Plot_Stacked_Graphs = Plot_Stacked_Graphs(self.frame_scripts, self.o_file_handler)
        self.o_Pole_fig = Plugin_Pole_fig(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)

        # help-stuff
        self.number_of_scripts = 4
        self.current_script = 0 # 0-none, 1-MOS, 2-XRD1, 3-Plot_stacked_graphs, 4-Pole-fig, 5-....

        self.callback_plot_xrd_button()


    def remove_files(self):
        self.o_file_handler.remove_all_files()


    def open_file(self):
        self.o_file_handler.new_file()

    def save_file(self):
        if self.current_script == 1:
            self.o_file_handler.save_file(self.o_MOS_script.get_results())
        elif self.current_script == 2:
            self.o_file_handler.save_file(self.o_XRD1_script.get_results())
        elif self.current_script == 4:
            self.o_file_handler.save_file(self.o_Pole_fig.get_results())

    def callback_mos_button(self):
        # Set MOS as current script!
        self.current_script = 1
        self.hide_all_script_settings()
        #highlight button
        self.highlight_script_button(self.current_script)
        # Show the MOS settings frame!
        self.o_MOS_script.show_frame()

    def callback_xrd1_button(self):
        # Set XRD1 as current script!
        self.current_script = 2
        self.hide_all_script_settings()
        # highlight button
        self.highlight_script_button(self.current_script)
        # Show the XRD-settings frame
        self.o_XRD1_script.show_frame()

    def callback_plot_xrd_button(self):
        # Set plot xrd as current script!
        self.current_script = 3
        self.hide_all_script_settings()
        # highlight button
        self.highlight_script_button(self.current_script)
        # Show the XRD-settings frame
        self.o_Plot_Stacked_Graphs.show_frame()

    def callback_pole_fig_button(self):
        # Set plot xrd as current script!
        self.current_script = 4
        self.hide_all_script_settings()
        # highlight button
        self.highlight_script_button(self.current_script)
        # Show the XRD-settings frame
        self.o_Pole_fig.show_frame()

    def hide_all_script_settings(self):
        self.o_MOS_script.hide_frame()
        self.o_XRD1_script.hide_frame()
        self.o_Plot_Stacked_Graphs.hide_frame()
        self.o_Pole_fig.hide_frame()

    def highlight_script_button(self, script_id):
        self.b_select_mos.config(bg=Defs.c_white)
        self.b_select_xrd1.config(bg=Defs.c_white)
        self.b_select_xrd_plot.config(bg=Defs.c_white)
        self.b_select_pole_fig.config(bg=Defs.c_white)

        if script_id == 1:
            self.b_select_mos.config(bg=Defs.c_button_active)

        elif script_id == 2:
            self.b_select_xrd1.config(bg=Defs.c_button_active)

        elif script_id == 3:
            self.b_select_xrd_plot.config(bg=Defs.c_button_active)

        elif script_id == 4:
            self.b_select_pole_fig.config(bg=Defs.c_button_active)
