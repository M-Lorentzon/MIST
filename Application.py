from File_Handler import *
from Text_Plotter import *
from Error_Handler import *


from Scripts_and_Plugins.Plugin_MOS import *
from Scripts_and_Plugins.Plugin_XRD1 import *
from Scripts_and_Plugins.Plugin_Stacked_Graphs import *
from Scripts_and_Plugins.Plugin_Pole_fig import *
from Scripts_and_Plugins.Plugin_Material_Calc import *
from Scripts_and_Plugins.Plugin_Nanoindentation import *
from Scripts_and_Plugins.Plugin_XPS_data import *
from Scripts_and_Plugins.Plugin_Asterix_PF import *
from Scripts_and_Plugins.Plugin_PIXE import *
from Scripts_and_Plugins.Plugin_SRIM import *
from Scripts_and_Plugins.Plugin_quick_scripts import *
from Scripts_and_Plugins.Plugin_Testing import *
from Scripts_and_Plugins.Plugin_Asterix_scans import *
from Scripts_and_Plugins.Plugin_Cantilever_Curves import *
from Scripts_and_Plugins.Plugin_RSM import *
from Scripts_and_Plugins.Plugin_RSM_Planning import *
from Scripts_and_Plugins.Plugin_PNR import *

from Scripts_and_Plugins.Plugin_Plot_2D_Integrated_WAX import *
from Scripts_and_Plugins.Plugin_2D_image import *
#from Scripts_and_Plugins.Fake_Plugin_2D_image import *
#from Scripts_and_Plugins.Fake_Plugin_Plot_2D_Integrated_WAX import *

from Scripts_and_Plugins.Plugin_Plasma_probe import *
from Scripts_and_Plugins.Plugin_Help_Others import *



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


        # frames in Info frame
        self.frame_info_global_buttons = tk.Frame(self.frame_info, bg=Defs.c_frame_color)
        self.frame_info_global_buttons.grid(column=0, row=1, sticky="NSEW", padx=5, pady=5)
        self.frame_info_script_buttons = tk.Frame(self.frame_info, bg=Defs.c_frame_color)
        self.frame_info_script_buttons.grid(column=0, row=2, sticky="NSEW", padx=5, pady=5)
        self.frame_info_file_handler = tk.Frame(self.frame_info, bg=Defs.c_frame_color)
        self.frame_info_file_handler.grid(column=1, row=1, sticky="NSEW", padx=5, pady=5, rowspan=4)
        self.frame_info_error_box = tk.Frame(self.frame_info, bg=Defs.c_frame_color)
        self.frame_info_error_box.grid(column=0, row=3, sticky="NSEW", padx=5, pady=5)

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
        self.b_select_pole_fig = tk.Button(self.frame_info_script_buttons, text="Pole-fig", command=self.callback_pole_fig_button)
        self.b_select_pole_fig.config(width=8)
        self.b_select_pole_fig.grid(row=1, column=2, sticky="NW")

        self.b_select_xps = tk.Button(self.frame_info_script_buttons, text="XPS_Data", command=self.callback_xps_button)
        self.b_select_xps.config(width=8)
        self.b_select_xps.grid(row=2, column=0, sticky="NW")
        self.b_select_pixe = tk.Button(self.frame_info_script_buttons, text="PIXE", command=self.callback_pixe_button)
        self.b_select_pixe.config(width=8)
        self.b_select_pixe.grid(row=2, column=1, sticky="NW")
        self.b_select_Asterix_PF = tk.Button(self.frame_info_script_buttons, text="Asterix PF", command=self.callback_asterix_PF)
        self.b_select_Asterix_PF.config(width=8)
        self.b_select_Asterix_PF.grid(row=2, column=2, sticky="NW")

        self.b_select_2d_image = tk.Button(self.frame_info_script_buttons, text="2D Image", command=self.callback_2D_Image_button)
        self.b_select_2d_image.config(width=8)
        self.b_select_2d_image.grid(row=3, column=0, sticky="NW")
        self.b_select_quick_script = tk.Button(self.frame_info_script_buttons, text="Quick script", command=self.callback_quick_script)
        self.b_select_quick_script.config(width=8)
        self.b_select_quick_script.grid(row=3, column=1, sticky="NW")
        self.b_select_srim = tk.Button(self.frame_info_script_buttons, text="SRIM", command=self.callback_SRIM_button)
        self.b_select_srim.config(width=8)
        self.b_select_srim.grid(row=3, column=2, sticky="NW")

        self.b_select_2D_WAX = tk.Button(self.frame_info_script_buttons, text="2D WAX", command=self.callback_2D_WAX_button)
        self.b_select_2D_WAX.config(width=8)
        self.b_select_2D_WAX.grid(row=4, column=0, sticky="NW")
        self.b_select_Plasma = tk.Button(self.frame_info_script_buttons, text="Plasma", command=self.callback_Plasma_Probe)
        self.b_select_Plasma.config(width=8)
        self.b_select_Plasma.grid(row=4, column=1, sticky="NW")
        self.b_select_RSM = tk.Button(self.frame_info_script_buttons, text="RSM", command=self.callback_RSM)
        self.b_select_RSM.config(width=8)
        self.b_select_RSM.grid(row=4, column=2, sticky="NW")

        self.b_select_Asterix_Scans = tk.Button(self.frame_info_script_buttons, text="Asterix scan", command=self.callback_Asterix_Scans)
        self.b_select_Asterix_Scans.config(width=8)
        self.b_select_Asterix_Scans.grid(row=5, column=0, sticky="NW")
        self.b_select_Cantilever = tk.Button(self.frame_info_script_buttons, text="Cantilever", command=self.callback_Cantilever_Curves)
        self.b_select_Cantilever.config(width=8)
        self.b_select_Cantilever.grid(row=5, column=1, sticky="NW")
        self.b_select_RSM_Planning = tk.Button(self.frame_info_script_buttons, text="Plan RSM", command=self.callback_RSM_Planning)
        self.b_select_RSM_Planning.config(width=8)
        self.b_select_RSM_Planning.grid(row=5, column=2, sticky="NW")

        self.b_select_Testing = tk.Button(self.frame_info_script_buttons, text="Testing", command=self.callback_Testing)
        self.b_select_Testing.config(width=8)
        self.b_select_Testing.grid(row=9, column=2, sticky="NW")
        self.b_select_PNR = tk.Button(self.frame_info_script_buttons, text="PNR", command=self.callback_PNR)
        self.b_select_PNR.config(width=8)
        self.b_select_PNR.grid(row=9, column=1, sticky="NW")
        self.b_select_Help_Others = tk.Button(self.frame_info_script_buttons, text="Help Others", command=self.callback_Help_Others)
        self.b_select_Help_Others.config(width=8)
        self.b_select_Help_Others.grid(row=9, column=0, sticky="NW")

        # Labels
        self.text_intro = tk.Label(self.frame_info, text=Defs.t_intro, bg=Defs.c_description_color)
        self.text_intro.grid(row=0, sticky="WE", columnspan=10)

        # Help objects!
        self.o_error_handler = Error_Handler(self.frame_info_error_box)
        self.o_file_handler = file_handler(self.frame_info_file_handler)
        self.o_Text_Plotter = Text_Plotter()

        # Script plugin classes to do the work
        self.o_MOS_script = None
        self.o_XRD1_script = None
        self.o_Plot_Stacked_Graphs = None
        self.o_Pole_fig = None
        self.o_material_calc = None
        self.o_nanoindentation = None
        self.o_xps_data = None
        self.o_PIXE = None
        self.o_asterix_PF = None
        self.o_SRIM = None
        self.o_2D_Image = None
        self.o_quick_script = None
        self.o_Plot_2D_Integrated_WAX = None
        self.o_Plasma_probe = None
        self.o_Testing = None
        self.o_asterix_scans = None
        self.o_cantilever_curves = None
        self.o_RSM = None
        self.o_Plan_RSM = None
        self.o_PNR = None
        self.o_Help_others = None

        # list of tuples containing activated and initiated scripts.
        self.activated_objects = []

        # Init-stuff
        self.o_error_handler.Write_notification("Welcome to MIST!")
        self.o_error_handler.Write_Error_Text("Red: Error message!")
        self.o_error_handler.Write_notification("Black: Notification!")

        # starting script
        self.callback_Help_Others()


    def remove_files(self):
        self.o_file_handler.remove_all_files()


    def open_file(self):
        self.o_file_handler.new_file()

    def save_file(self):

        for object_tuple in self.activated_objects:
            if object_tuple[0].active:
                if object_tuple[0].savable_script:
                    self.o_file_handler.save_file(object_tuple[0].get_results())
                else:
                    self.o_error_handler.Write_Error_Text("Tried to save a new file from a script which is defined as not savable")

    def callback_mos_button(self):
        if self.o_MOS_script is None:
            self.o_MOS_script = MOS_Script(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
            self.activated_objects.append((self.o_MOS_script, self.b_select_mos))
        self.reset_active_script()
        self.o_MOS_script.show_frame()
        self.o_MOS_script.active = True
        self.highlight_script_button()

    def callback_xrd1_button(self):
        if self.o_XRD1_script is None:
            self.o_XRD1_script = Plugin_XRD1(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
            self.activated_objects.append((self.o_XRD1_script, self.b_select_xrd1))
        self.reset_active_script()
        self.o_XRD1_script.show_frame()
        self.o_XRD1_script.active = True
        self.highlight_script_button()

    def callback_plot_xrd_button(self):
        if self.o_Plot_Stacked_Graphs is None:
            self.o_Plot_Stacked_Graphs = Plugin_Stacked_Graphs(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_Plot_Stacked_Graphs, self.b_select_xrd_plot))
        self.reset_active_script()
        self.o_Plot_Stacked_Graphs.show_frame()
        self.o_Plot_Stacked_Graphs.active = True
        self.highlight_script_button()

    def callback_pole_fig_button(self):
        if self.o_Pole_fig is None:
            self.o_Pole_fig = Plugin_Pole_fig(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
            self.activated_objects.append((self.o_Pole_fig, self.b_select_pole_fig))
        self.reset_active_script()
        self.o_Pole_fig.show_frame()
        self.o_Pole_fig.active = True
        self.highlight_script_button()

    def callback_material_calc_button(self):
        if self.o_material_calc is None:
            self.o_material_calc = Plugin_Material_Calc(self.frame_scripts)
            self.activated_objects.append((self.o_material_calc, self.b_select_mater_calc))
        self.reset_active_script()
        self.o_material_calc.show_frame()
        self.o_material_calc.active = True
        self.highlight_script_button()

    def callback_nanoindent_button(self):
        if self.o_nanoindentation is None:
            self.o_nanoindentation = Plugin_Nanoindent(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_nanoindentation, self.b_select_nanoindent))
        self.reset_active_script()
        self.o_nanoindentation.show_frame()
        self.o_nanoindentation.active = True
        self.highlight_script_button()

    def callback_xps_button(self):
        if self.o_xps_data is None:
            self.o_xps_data = Plugin_XPS_data(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_xps_data, self.b_select_xps))
        self.reset_active_script()
        self.o_xps_data.show_frame()
        self.o_xps_data.active= True
        self.highlight_script_button()

    def callback_pixe_button(self):
        if self.o_PIXE is None:
            self.o_PIXE = Plugin_PIXE(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_PIXE, self.b_select_pixe))
        self.reset_active_script()
        self.o_PIXE.show_frame()
        self.o_PIXE.active= True
        self.highlight_script_button()

    def callback_asterix_PF(self):
        if self.o_asterix_PF is None:
            self.o_asterix_PF = Plugin_Asterix_PF(self.frame_scripts, self.o_file_handler, self.o_Text_Plotter)
            self.activated_objects.append((self.o_asterix_PF, self.b_select_Asterix_PF))
        self.reset_active_script()
        self.o_asterix_PF.show_frame()
        self.o_asterix_PF.active = True
        self.highlight_script_button()

    def callback_SRIM_button(self):
        if self.o_SRIM is None:
            self.o_SRIM = Plugin_SRIM(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_SRIM, self.b_select_srim))
        self.reset_active_script()
        self.o_SRIM.show_frame()
        self.o_SRIM.active= True
        self.highlight_script_button()

    def callback_2D_Image_button(self):
        if self.o_2D_Image is None:
            self.o_2D_Image = Plugin_2D_Image(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_2D_Image, self.b_select_2d_image))
        self.reset_active_script()
        self.o_2D_Image.show_frame()
        self.o_2D_Image.active = True
        self.highlight_script_button()

    def callback_2D_WAX_button(self):
        if self.o_Plot_2D_Integrated_WAX is None:
            self.o_Plot_2D_Integrated_WAX = Plugin_Plot_2D_Integrated_WAX(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_Plot_2D_Integrated_WAX, self.b_select_2D_WAX))
        self.reset_active_script()
        self.o_Plot_2D_Integrated_WAX.show_frame()
        self.o_Plot_2D_Integrated_WAX.active = True
        self.highlight_script_button()


    def callback_RSM(self):
        if self.o_RSM is None:
            self.o_RSM = Plugin_RSM(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_RSM, self.b_select_RSM))
        self.reset_active_script()
        self.o_RSM.show_frame()
        self.o_RSM.active = True
        self.highlight_script_button()

    def callback_RSM_Planning(self):
        if self.o_Plan_RSM is None:
            self.o_Plan_RSM = Plugin_RSM_Planning(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_Plan_RSM,self.b_select_RSM_Planning))
        self.reset_active_script()
        self.o_Plan_RSM.show_frame()
        self.o_Plan_RSM.active = True
        self.highlight_script_button()

    def callback_Plasma_Probe(self):
        if self.o_Plasma_probe is None:
            self.o_Plasma_probe = Plugin_Plasma_probe(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_Plasma_probe, self.b_select_Plasma))
        self.reset_active_script()
        self.o_Plasma_probe.show_frame()
        self.o_Plasma_probe.active = True
        self.highlight_script_button()

    def callback_Asterix_Scans(self):
        if self.o_asterix_scans is None:
            self.o_asterix_scans = Plugin_Asterix_scans(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_asterix_scans, self.b_select_Asterix_Scans))
        self.reset_active_script()
        self.o_asterix_scans.show_frame()
        self.o_asterix_scans.active = True
        self.highlight_script_button()

    def callback_Cantilever_Curves(self):
        if self.o_cantilever_curves is None:
            self.o_cantilever_curves = Plugin_Cantilever_Curves(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_cantilever_curves, self.b_select_Cantilever))
        self.reset_active_script()
        self.o_cantilever_curves.show_frame()
        self.o_cantilever_curves.active = True
        self.highlight_script_button()

    def callback_quick_script(self):
        if self.o_quick_script is None:
            self.o_quick_script = Plugin_Quick_Script(self.frame_scripts)
            self.activated_objects.append((self.o_quick_script, self.b_select_quick_script))
        self.reset_active_script()
        self.o_quick_script.show_frame()
        self.o_quick_script.active = True
        self.highlight_script_button()

    def callback_Testing(self):
        if self.o_Testing is None:
            self.o_Testing = Plugin_Testing(self.frame_scripts, self.o_file_handler, self.o_error_handler)
            self.activated_objects.append((self.o_Testing, self.b_select_Testing))
        self.reset_active_script()
        self.o_Testing.show_frame()
        self.o_Testing.active = True
        self.highlight_script_button()

    def callback_PNR(self):
        if self.o_PNR is None:
            self.o_PNR = Plugin_PNR(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_PNR, self.b_select_PNR))
        self.reset_active_script()
        self.o_PNR.show_frame()
        self.o_PNR.active = True
        self.highlight_script_button()

    def callback_Help_Others(self):
        if self.o_Help_others is None:
            self.o_Help_others = Plugin_Help_Others(self.frame_scripts, self.o_file_handler)
            self.activated_objects.append((self.o_Help_others, self.b_select_Help_Others))
        self.reset_active_script()
        self.o_Help_others.show_frame()
        self.o_Help_others.active = True
        self.highlight_script_button()


    def reset_active_script(self):
        for object_tuble in self.activated_objects:
            object_tuble[0].hide_frame()
            object_tuble[0].active = False

    def highlight_script_button(self):
        for object_tuble in self.activated_objects:
            if object_tuble[0].active:
                object_tuble[1].config(bg=Defs.c_button_active)
            else:
                object_tuble[1].config(bg=Defs.c_white)