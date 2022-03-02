from File_Handler import *
from Text_Plotter import *
from Error_Handler import *
from Scripts_and_Plugins.Plugin_MOS import *
from Scripts_and_Plugins.Plugin_XRD1 import *
from Scripts_and_Plugins.Plot_Stacked_Graphs import *
from Scripts_and_Plugins.Plugin_Pole_fig import *
from Scripts_and_Plugins.Plugin_Material_Calc import *
from Scripts_and_Plugins.Plugin_Nanoindentation import *

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
        self.frame_info_error_box = tk.Frame(self.frame_info, bg=Defs.c_frame_color)
        self.frame_info_error_box.grid(column=0, row=4, sticky="NSEW", padx=20, pady=5)

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
        self.b_select_mater_calc = tk.Button(self.frame_info_script_buttons, text="Mat.Calc", command=self.callback_material_calc_button)
        self.b_select_mater_calc.config(width=8)
        self.b_select_mater_calc.grid(row=0, column=1, sticky="NW")
        self.b_select_nanoindent = tk.Button(self.frame_info_script_buttons, text="Nanoind", command=self.callback_nanoindent_button)
        self.b_select_nanoindent.config(width=8)
        self.b_select_nanoindent.grid(row=0, column=2, sticky="NW")

        self.b_select_xrd1 = tk.Button(self.frame_info_script_buttons, text="XRD1", command=self.callback_xrd1_button)
        self.b_select_xrd1.config(width=8)
        self.b_select_xrd1.grid(row=1, column=0, sticky="NW")
        self.b_select_xrd_plot = tk.Button(self.frame_info_script_buttons, text="Plot_XRD", command=self.callback_plot_xrd_button)
        self.b_select_xrd_plot.config(width=8)
        self.b_select_xrd_plot.grid(row=1, column=1, sticky="NW")
        self.b_select_pole_fig = tk.Button(self.frame_info_script_buttons, text="Pole-fig",command=self.callback_pole_fig_button)
        self.b_select_pole_fig.config(width=8)
        self.b_select_pole_fig.grid(row=1, column=2, sticky="NW")

        # Labels
        self.text_intro = tk.Label(self.frame_info, text=Defs.t_intro, bg=Defs.c_description_color)
        self.text_intro.grid(row=0, sticky="WE", columnspan=10)

        # Help objects!
        self.o_error_handler = Error_Handler(self.frame_info_error_box)
        self.o_file_handler = file_handler(self.frame_info_file_handler)
        self.o_Text_Plotter = Text_Plotter(self.frame_view)

        # Script plugin classes to do the work
        self.o_MOS_script = MOS_Script(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
        self.o_XRD1_script = Plugin_XRD1(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
        self.o_Plot_Stacked_Graphs = Plot_Stacked_Graphs(self.frame_scripts, self.o_file_handler)
        self.o_Pole_fig = Plugin_Pole_fig(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
        self.o_material_calc = Plugin_Material_Calc(self.frame_scripts)
        self.o_nanoindentation = Plugin_Nanoindent(self.frame_scripts, self.o_file_handler)

        self.list_of_objects = [(self.o_MOS_script, self.b_select_mos), (self.o_XRD1_script, self.b_select_xrd1),
                                (self.o_Plot_Stacked_Graphs, self.b_select_xrd_plot), (self.o_Pole_fig, self.b_select_pole_fig),
                                (self.o_material_calc, self.b_select_mater_calc), (self.o_nanoindentation, self.b_select_nanoindent)]

        # Init-stuff
        self.o_error_handler.Write_notification("Welcome to MIST!")
        self.o_error_handler.Write_Error_Text("Red: Error message!")
        self.o_error_handler.Write_notification("Black: Notification!")

        # starting script
        self.callback_nanoindent_button()


    def remove_files(self):
        self.o_file_handler.remove_all_files()


    def open_file(self):
        self.o_file_handler.new_file()

    def save_file(self):

        for object_tuple in self.list_of_objects:
            if object_tuple[0].active:
                if object_tuple[0].savable_script:
                    self.o_file_handler.save_file(object_tuple[0].get_results())
                else:
                    self.o_error_handler.Write_Error_Text("Tried to save a new file from a script which is defined as not savable")

    def callback_mos_button(self):
        self.reset_active_script()
        self.o_MOS_script.show_frame()
        self.o_MOS_script.active = True
        self.highlight_script_button()

    def callback_xrd1_button(self):
        self.reset_active_script()
        self.o_XRD1_script.show_frame()
        self.o_XRD1_script.active = True
        self.highlight_script_button()

    def callback_plot_xrd_button(self):
        self.reset_active_script()
        self.o_Plot_Stacked_Graphs.show_frame()
        self.o_Plot_Stacked_Graphs.active = True
        self.highlight_script_button()

    def callback_pole_fig_button(self):
        self.reset_active_script()
        self.o_Pole_fig.show_frame()
        self.o_Pole_fig.active = True
        self.highlight_script_button()

    def callback_material_calc_button(self):
        self.reset_active_script()
        self.o_material_calc.show_frame()
        self.o_material_calc.active = True
        self.highlight_script_button()

    def callback_nanoindent_button(self):
        self.reset_active_script()
        self.o_nanoindentation.show_frame()
        self.o_nanoindentation.active = True
        self.highlight_script_button()

    def reset_active_script(self):
        for object_tuble in self.list_of_objects:
            object_tuble[0].hide_frame()
            object_tuble[0].active = False

    def highlight_script_button(self):
        for object_tuble in self.list_of_objects:
            if object_tuble[0].active:
                object_tuble[1].config(bg=Defs.c_button_active)
            else:
                object_tuble[1].config(bg=Defs.c_white)