import tkinter as tk
from Util.My_Float_Entry import My_Float_Entry
from Util.My_Label_Entry import My_Label_Entry
from Util.color_selector import Color_Selector

import tkscrolledframe as SF
import matplotlib.pyplot as plt
import Util.Definitions as Defs
import user_config.PFD_Settings_Handler as PDF_Settings

from math import log1p
from math import sqrt

Description = """This script is a plotting tool for stacked lines
especially for XRD data (.xy files).
 
First open the files you want to use and import 
them into the script environment either one by one
or all opened files at once.

Use the entries and buttons to modify the plot 
according to your needs, and click 'Plot'. 

Predefined powder diffraction files are available
and you can draw own lines and texts.

Redrawing the figure using 'Plot' will overwrite 
any additional lines or texts.
 
"""



class Plot_Stacked_Graphs:

    def __init__(self, Script_frame, file_handler):
        self.script_frame = Script_frame # shared with all scripts
        self.o_file_handler = file_handler # to get data from
        self.o_pdf_settings = PDF_Settings.PDF_Settings_Handler(self)

        self.active = False
        self.savable_script = False

        # Private frames
        self.my_frame = tk.Frame(self.script_frame, bg=Defs.c_script_entries) # Master within this scope

        self.sframe = SF.ScrolledFrame(self.my_frame, width=400, height=260)
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
        self.entry_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.entry_frame.grid(row=5, column=0)

        self.add_PDFs_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.add_PDFs_frame.grid(row=6, column=0)
        self.add_plot_text_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.add_plot_text_frame.grid(row=7, column=0)
        self.add_line_to_plot_frame = tk.Frame(self.my_frame, highlightbackground="black", highlightthickness=1, bg=Defs.c_script_entries)
        self.add_line_to_plot_frame.grid(row=8, column=0)

        # Master label
        self.label = tk.Label(self.my_frame, text="XRD stacked lines settings", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0)
        self.label.config(font=('Helvetica', 12, 'bold'))
        # Master description text
        self.text = tk.Text(self.my_frame, width=50, height=20, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, Description)
        self.text.config(state='disabled')

        # Entries
        self.Entry_offset = My_Float_Entry(self.entry_frame, "Multi-graph offset", 1, 0, 0)
        self.Entry_Line_Thickn = My_Float_Entry(self.entry_frame, "Graph line thickness", 0.5, 0, 1)
        self.Entry_title = My_Label_Entry(self.entry_frame, "Figure title", 1, 0, 4)
        self.Entry_PDF_thickness = My_Float_Entry(self.entry_frame, "PDF-line thickness", 0.09, 1, 1)

        # 'Add line to plot' stuff
        self.b_add_line = tk.Button(self.add_line_to_plot_frame, text="Add line", command=self.callback_add_line)
        self.b_add_line.grid(row=0, column=0, sticky="NW")
        self.Entry_line_label = My_Label_Entry(self.add_line_to_plot_frame, "Label", 0, 1, 4)
        self.Entry_line_x_pos = My_Float_Entry(self.add_line_to_plot_frame, "x-pos", 30, 1, 0)
        self.Entry_line_y_height = My_Float_Entry(self.add_line_to_plot_frame, "height (y)", 4, 1, 1)
        self.Entry_line_thickness = My_Float_Entry(self.add_line_to_plot_frame, "Thickness", 0.2, 1, 2)
        self.Entry_line_color = Color_Selector(self.add_line_to_plot_frame, "black", 1, 3)

        # "add text to plot" stuff
        self.b_add_text = tk.Button(self.add_plot_text_frame, text="Add text", command=self.callback_add_text)
        self.b_add_text.grid(row=0, column=0, sticky="NW")
        self.Entry_text_label = My_Label_Entry(self.add_plot_text_frame, "Text", 0, 1, 4)
        self.Entry_text_x_pos = My_Float_Entry(self.add_plot_text_frame, "x-pos", 0, 1, 0)
        self.Entry_text_y_pos = My_Float_Entry(self.add_plot_text_frame, "y-pos", 0, 1, 1)
        self.Entry_text_color = Color_Selector(self.add_plot_text_frame, "black", 1, 2)

        # Master Buttons
        self.b_import = tk.Button(self.master_button_frame, text="Import", command=self.callback_import_button)
        self.b_import.config(width=8)
        self.b_import.grid(row=0, column=0, sticky="NW")
        self.b_import_all = tk.Button(self.master_button_frame, text="Import All", command=self.callback_import_all_button)
        self.b_import_all.config(width=8)
        self.b_import_all.grid(row=0, column=1, sticky="NW")
        self.b_plot = tk.Button(self.master_button_frame, text="Plot", command=self.callback_plot_button)
        self.b_plot.config(width=8)
        self.b_plot.grid(row=0, column=2, sticky="NW")
        self.b_clear_files = tk.Button(self.master_button_frame, text="Clear files", command=self.callback_clear_files_button)
        self.b_clear_files.config(width=8)
        self.b_clear_files.grid(row=0, column=3, sticky="NW")
        self.b_settings = tk.Button(self.master_button_frame, text="Settings", command=self.callback_settings)
        self.b_settings.config(width=8)
        self.b_settings.grid(row=0, column=4, sticky="NW")

        # Selection buttons
        self.selection_index = 1
        self.b_linear = tk.Button(self.select_button_frame, text="Linear", command=self.callback_linear_button)
        self.b_linear.grid(row=5, column=0, sticky="NW")
        self.b_log = tk.Button(self.select_button_frame, text="Log", command=self.callback_log_button)
        self.b_log.grid(row=5, column=1, sticky="NW")
        self.b_sqrt = tk.Button(self.select_button_frame, text="SQRT", command=self.callback_sqrt_button)
        self.b_sqrt.grid(row=5, column=2, sticky="NW")

        # Add PDF buttons and more
        self.Entry_Bar_Height = My_Float_Entry(self.add_PDFs_frame, "PDF height", 4, 0, 1, 4)
        #self.PDF_Label = tk.Label(self.add_PDFs_frame, text="Predef PDF-data")
        #self.PDF_Label.grid(row=0, column=0, columnspan=9, sticky="NW")

        self.b_add_PDF1 = tk.Button(self.add_PDFs_frame, text=" Temp1 ", command=self.callback_add_PDF1)
        self.b_add_PDF1.grid(row=2, column=0, sticky="NW", padx=2)
        self.b_add_PDF1.config(text=self.o_pdf_settings.PDF_Data_Containers[self.o_pdf_settings.active_pdf[0]].name, bg=Defs.c_pdf_buttons)
        self.coPDF1 = Color_Selector(self.add_PDFs_frame, "blue", 2, 1)

        self.b_add_PDF2 = tk.Button(self.add_PDFs_frame, text=" Temp1 ", command=self.callback_add_PDF2)
        self.b_add_PDF2.grid(row=2, column=2, sticky="NW", padx=2)
        self.b_add_PDF2.config(text=self.o_pdf_settings.PDF_Data_Containers[self.o_pdf_settings.active_pdf[1]].name, bg=Defs.c_pdf_buttons)
        self.coPDF2 = Color_Selector(self.add_PDFs_frame, "purple", 2, 3)

        self.b_add_PDF3 = tk.Button(self.add_PDFs_frame, text=" Temp1 ", command=self.callback_add_PDF3)
        self.b_add_PDF3.grid(row=3, column=0, sticky="NW", padx=2)
        self.b_add_PDF3.config(text=self.o_pdf_settings.PDF_Data_Containers[self.o_pdf_settings.active_pdf[2]].name, bg=Defs.c_pdf_buttons)
        self.coPDF3 = Color_Selector(self.add_PDFs_frame, "red", 3, 1)

        self.b_add_PDF4 = tk.Button(self.add_PDFs_frame, text=" Temp1 ", command=self.callback_add_PDF4)
        self.b_add_PDF4.grid(row=3, column=2, sticky="NW", padx=2)
        self.b_add_PDF4.config(text=self.o_pdf_settings.PDF_Data_Containers[self.o_pdf_settings.active_pdf[3]].name, bg=Defs.c_pdf_buttons)
        self.coPDF4 = Color_Selector(self.add_PDFs_frame, "green", 3, 3)

        # File data imported in form of container class
        self.no_files_index = 0
        self.file_data = []
        self.data_labels = []

        # Setup correctly
        self.callback_log_button()

    def callback_add_line(self):
        xval = self.Entry_line_x_pos.get_value()
        yval = self.Entry_line_y_height.get_value()
        text = self.Entry_line_label.get_value()
        color = self.Entry_line_color.get_color()
        line_thickness = self.Entry_line_thickness.get_value()
        plt.bar(xval, height=yval, width=line_thickness, color=color)
        plt.text(xval, yval-1, text, {'ha': 'right'}, rotation=90, color=color)
        plt.show()

    def callback_add_text(self):
        xval = self.Entry_text_x_pos.get_value()
        yval = self.Entry_text_y_pos.get_value()
        text = self.Entry_text_label.get_value()
        color = self.Entry_text_color.get_color()
        plt.text(xval, yval, text, color=color)
        plt.show()

    def callback_add_PDF1(self):
        PDF_Cont = self.o_pdf_settings.get_active_pdf_container(0)
        color = self.coPDF1.get_color()
        self.plot_lines_from_tuples(PDF_Cont.get_list_of_active_data(), color)

    def callback_add_PDF2(self):
        PDF_Cont = self.o_pdf_settings.get_active_pdf_container(1)
        color = self.coPDF2.get_color()
        self.plot_lines_from_tuples(PDF_Cont.get_list_of_active_data(), color)

    def callback_add_PDF3(self):
        PDF_Cont = self.o_pdf_settings.get_active_pdf_container(2)
        color = self.coPDF3.get_color()
        self.plot_lines_from_tuples(PDF_Cont.get_list_of_active_data(), color)

    def callback_add_PDF4(self):
        PDF_Cont = self.o_pdf_settings.get_active_pdf_container(3)
        color = self.coPDF4.get_color()
        self.plot_lines_from_tuples(PDF_Cont.get_list_of_active_data(), color)

    def Update_PDF_Buttons(self):
        self.b_add_PDF1.config(text=self.o_pdf_settings.get_active_pdf_container(0).name)
        self.b_add_PDF2.config(text=self.o_pdf_settings.get_active_pdf_container(1).name)
        self.b_add_PDF3.config(text=self.o_pdf_settings.get_active_pdf_container(2).name)
        self.b_add_PDF4.config(text=self.o_pdf_settings.get_active_pdf_container(3).name)

    def plot_lines_from_tuples(self, t_list, color):
        y_val = self.Entry_Bar_Height.get_value()
        for tup in t_list:
            plt.bar(tup[0], height=y_val, width=self.Entry_PDF_thickness.get_value(), color=color, linestyle="-")
            plt.text(tup[0], y_val-1, tup[1], {'ha': 'right'}, rotation=90, color=color)
        plt.show()

    def callback_clear_files_button(self):
        self.no_files_index = 0
        for label_ in self.data_labels :
            label_.hide()
        self.file_data[:] = []
        self.data_labels[:] = []
        plt.clf()

    def callback_settings(self):
        self.o_pdf_settings.Open_Settings()

    def callback_linear_button(self):
        self.selection_index = 0
        self.unmark_select_buttons()
        self.b_linear.config(bg=Defs.c_button_active)

    def callback_log_button(self):
        self.selection_index = 1
        self.unmark_select_buttons()
        self.b_log.config(bg=Defs.c_button_active)

    def callback_sqrt_button(self):
        self.selection_index = 2
        self.unmark_select_buttons()
        self.b_sqrt.config(bg=Defs.c_button_active)

    def callback_plot_button(self):
        plt.clf()
        Number_of_graphs = len(self.file_data)

        for file_index in range(len(self.file_data)):
            angles = self.file_data[file_index].Column1
            label = self.data_labels[file_index].get_value()
            offset = self.Entry_offset.get_value() * (Number_of_graphs - file_index)
            Line_thickness = self.Entry_Line_Thickn.get_value()

            if self.selection_index == 0: #linear
                plt.plot(angles, self.file_data[file_index].get_col2_in_linear_with_offset(offset), label=label, linewidth=Line_thickness)
                plt.ylabel("Intensity (linear, a.u)")
            elif self.selection_index == 1: #log
                plt.plot(angles, self.file_data[file_index].get_col2_in_log_with_offset(offset), label=label, linewidth=Line_thickness)
                plt.ylabel("Intensity (log10, a.u)")
            elif self.selection_index == 2: #sqrt
                plt.plot(angles, self.file_data[file_index].get_col2_in_sqrt_with_offset(offset), label=label, linewidth=Line_thickness)
                plt.ylabel("Intensity (sqrt, a.u)")
            else:
                print("Error in selecting lin, log or sqrt")
        plt.title(self.Entry_title.get_value())
        plt.xlabel('2theta')
        plt.legend()
        plt.legend().set_draggable(True)
        plt.show()

    def callback_import_all_button(self):
        for data_in_file in self.o_file_handler.List_of_file_contents:
            self.no_files_index += 1
            data_in_file.extract_columns()
            self.file_data.append(data_in_file)

            new_entry = My_Label_Entry(self.label_entry_frame, data_in_file.file_name, self.no_files_index, 0)
            new_entry.set_label_bg("seagreen1")
            new_entry.set_entry_value(data_in_file.file_name)
            self.data_labels.append(new_entry)

    def callback_import_button(self):
        self.no_files_index += 1
        data = self.o_file_handler.get_current_data()
        data.extract_columns()
        self.file_data.append(data)

        new_entry = My_Label_Entry(self.label_entry_frame, data.file_name, self.no_files_index, 0)
        new_entry.set_entry_value(data.file_name)
        new_entry.set_label_bg("seagreen1")
        self.data_labels.append(new_entry)

    def unmark_select_buttons(self):
        self.b_linear.config(bg=Defs.c_button_inactive)
        self.b_log.config(bg=Defs.c_button_inactive)
        self.b_sqrt.config(bg=Defs.c_button_inactive)

    def show_frame(self):
        self.my_frame.grid(column=0, row=0, sticky="NSEW")

    def hide_frame(self):
        self.my_frame.grid_forget()





