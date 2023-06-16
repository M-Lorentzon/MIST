import tkinter as tk
import Util.Definitions as Defs
import Util.My_Checkbutton
import PDF_user_config.PDF_Data as PDF
from Util.My_Label_Entry import My_Label_Entry
from Util.My_PDF_Card_Entry import My_PDF_Card_Entry
from Util.My_PDF_Entry_Interactive import My_PDF_Entry_Interactive
import tkscrolledframe as SF

descr_new = """Add new PDF to the list of available
cards. Lines where 2theta = 0 is 
ignored. 
"""

descr_modify = """Modify a PDF by selecting one card 
only. You can write new/change a peak
specification or you can remove it by
setting 2theta = 0. Setting all 2theta
to 0 will remove the card.
You can select which peaks should be 
plotted.
"""

descr_swap = """This page changes which PDF-card is
selectable to plot by the buttons.
Select one (and only one) golden button 
box and one (and only one) blue card 
box.
"""

class popup_settings:

    def __init__(self, parent):
        self.Parent = parent
        self.popup_window = tk.Toplevel(bg=Defs.c_frame_color)

        self.popup_window.geometry("550x500")
        self.popup_window.title("PDF file settings")

        # Frames
        self.operation_selection_frame = tk.Frame(self.popup_window, bg=Defs.c_script_entries)
        self.operation_selection_frame.grid(row=0, column=0, sticky="EW")
        self.accept_decline_frame = tk.Frame(self.popup_window, bg=Defs.c_script_entries)
        self.accept_decline_frame.grid(row=10, column=0, sticky="EW")

        self.new_PDF_frame = tk.Frame(self.popup_window, bg=Defs.c_script_entries)
        self.mod_PDF_frame = tk.Frame(self.popup_window, bg=Defs.c_script_entries)
        self.swap_PDF_frame = tk.Frame(self.popup_window, bg=Defs.c_script_entries)

        self.sframe1 = SF.ScrolledFrame(self.new_PDF_frame, width=280, height=200)
        self.sframe1.grid(row=5, column=0, columnspan=3)
        self.sframe1.config(bg=Defs.c_frame_color)
        self.sframe1.bind_arrow_keys(self.new_PDF_frame)
        self.sframe1.bind_scroll_wheel(self.new_PDF_frame)
        self.new_PDF_frame_scrolled = self.sframe1.display_widget(tk.Frame)
        self.new_PDF_frame_scrolled.config(bg=Defs.c_frame_color)

        self.sframe2 = SF.ScrolledFrame(self.mod_PDF_frame, width=110, height=200)
        self.sframe2.grid(row=2, column=0, rowspan=10)
        self.sframe2.config(bg=Defs.c_frame_color)
        self.sframe2.bind_arrow_keys(self.mod_PDF_frame)
        self.sframe2.bind_scroll_wheel(self.mod_PDF_frame)
        self.mod_PDF_frame_scrolled1 = self.sframe2.display_widget(tk.Frame)
        self.mod_PDF_frame_scrolled1.config(bg=Defs.c_frame_color)

        self.sframe3 = SF.ScrolledFrame(self.mod_PDF_frame, width=370, height=200)
        self.sframe3.grid(row=2, column=1, rowspan=10)
        self.sframe3.config(bg=Defs.c_frame_color)
        self.sframe3.bind_arrow_keys(self.mod_PDF_frame)
        self.sframe3.bind_scroll_wheel(self.mod_PDF_frame)
        self.mod_PDF_frame_scrolled2 = self.sframe3.display_widget(tk.Frame)
        self.mod_PDF_frame_scrolled2.config(bg=Defs.c_frame_color)

        self.sframe4 = SF.ScrolledFrame(self.swap_PDF_frame, width=150, height=150)
        self.sframe4.grid(row=5, column=0, columnspan=3)
        self.sframe4.config(bg=Defs.c_frame_color)
        self.sframe4.bind_arrow_keys(self.swap_PDF_frame)
        self.sframe4.bind_scroll_wheel(self.swap_PDF_frame)
        self.swap_PDF_frame_scrolled = self.sframe4.display_widget(tk.Frame)
        self.swap_PDF_frame_scrolled.config(bg=Defs.c_frame_color)

        self.selection_indication = 0 # 0=New, 1=mod, 2=swap
        self.callback_new_pdf_button()

        # Master label
        self.label = tk.Label(self.operation_selection_frame, text="Change settings", bg=Defs.c_script_name)
        self.label.grid(row=0, column=0, columnspan=4)
        self.label.config(font=('Helvetica', 12, 'bold'))

        # Selection buttons and accept buttons
        self.b_new_pdf = tk.Button(self.operation_selection_frame, text="New PDF", command=self.callback_new_pdf_button)
        self.b_new_pdf.config(width=8)
        self.b_new_pdf.grid(row=1, column=0, sticky="NW")
        self.b_mod_pdf = tk.Button(self.operation_selection_frame, text="Mod. PDF", command=self.callback_mod_pdf_button)
        self.b_mod_pdf.config(width=8)
        self.b_mod_pdf.grid(row=1, column=1, sticky="NW")
        self.b_swap_pdf = tk.Button(self.operation_selection_frame, text="swap PDF", command=self.callback_swap_pdf_button)
        self.b_swap_pdf.config(width=8)
        self.b_swap_pdf.grid(row=1, column=2, sticky="NW")


        self.b_OK_pdf = tk.Button(self.accept_decline_frame, text="OK", command=self.callback_OK_button)
        self.b_OK_pdf.config(width=8)
        self.b_OK_pdf.grid(row=0, column=0, sticky="NW")
        self.b_cancel = tk.Button(self.accept_decline_frame, text="Cancel", command=self.callback_Cancel_button)
        self.b_cancel.config(width=8)
        self.b_cancel.grid(row=0, column=1, sticky="NW")


        #### Swap PDF stuff ####
        self.label_swap = tk.Label(self.swap_PDF_frame, text="Swap a PDF button", bg=Defs.c_script_name)
        self.label_swap.grid(row=0, column=0)
        self.label_swap.config(font=('Helvetica', 10, 'bold'))

        self.text = tk.Text(self.swap_PDF_frame, width=40, height=8, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, descr_swap)
        self.text.config(state='disabled')

        self.active_pdf_list_swap = []
        self.total_pdf_list_swap = []

        self.active_pdf_list_swap.append(Util.My_Checkbutton.My_Checkbutton(self.swap_PDF_frame, self.function_swap_pdf,
                                                                            self.Parent.PDF_Data_Containers[self.Parent.active_pdf[0]].name, 2, 0))
        self.active_pdf_list_swap.append(Util.My_Checkbutton.My_Checkbutton(self.swap_PDF_frame, self.function_swap_pdf,
                                                                            self.Parent.PDF_Data_Containers[self.Parent.active_pdf[1]].name, 2, 1))

        self.active_pdf_list_swap.append(Util.My_Checkbutton.My_Checkbutton(self.swap_PDF_frame, self.function_swap_pdf,
                                                                            self.Parent.PDF_Data_Containers[self.Parent.active_pdf[2]].name, 3, 0))
        self.active_pdf_list_swap.append(Util.My_Checkbutton.My_Checkbutton(self.swap_PDF_frame, self.function_swap_pdf,
                                                                            self.Parent.PDF_Data_Containers[self.Parent.active_pdf[3]].name, 3, 1))

        increment = 0
        for card in self.Parent.PDF_Data_Containers:
            self.total_pdf_list_swap.append(Util.My_Checkbutton.My_Checkbutton(self.swap_PDF_frame_scrolled, self.function_swap_pdf,
                                                                               card.name, 4 + increment, 0))
            increment += 1

        for button in self.total_pdf_list_swap:
            button.set_checkbutton_layout_two()
        for button in self.active_pdf_list_swap:
            button.set_checkbutton_layout_one()


        #### New PDF stuff ####
        self.label_new = tk.Label(self.new_PDF_frame, text="New PDF", bg=Defs.c_script_name)
        self.label_new.grid(row=0, column=0)
        self.label_new.config(font=('Helvetica', 10, 'bold'))

        self.text = tk.Text(self.new_PDF_frame, width=40, height=8, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, descr_new)
        self.text.config(state='disabled')

        self.e_name = My_Label_Entry(self.new_PDF_frame, "Name: ", 2, 0)
        self.new_entries = []
        for i in range(15): # Make 15 entries!
            self.new_entries.append(My_PDF_Card_Entry(self.new_PDF_frame_scrolled, "", 0, 0, i+3, 0))

        #### Mod PDF stuff ####
        self.label_mod = tk.Label(self.mod_PDF_frame, text="Modify a PDF", bg=Defs.c_script_name)
        self.label_mod.grid(row=0, column=0)
        self.label_mod.config(font=('Helvetica', 10, 'bold'))

        self.text = tk.Text(self.mod_PDF_frame, width=40, height=8, bg=Defs.c_description_color)
        self.text.grid(row=1, column=0, columnspan=20)
        self.text.insert(0.0, descr_modify)
        self.text.config(state='disabled')


        self.total_list_of_pdfs_checkbuttons = []
        self.total_list_of_active_PDFs_peaks = []

        for index in range(len(self.Parent.PDF_Data_Containers)):
            self.total_list_of_pdfs_checkbuttons.append(
                Util.My_Checkbutton.My_Checkbutton(self.mod_PDF_frame_scrolled1, self.function_modify_PDF,
                                                   self.Parent.PDF_Data_Containers[index].name, 5+index, 0))

        for button in self.total_list_of_pdfs_checkbuttons:
            button.set_checkbutton_layout_two()

    def function_modify_PDF(self):
        # Change in which PDF has been selected/deselected
        for index in range(len(self.total_list_of_pdfs_checkbuttons)):
            if self.total_list_of_pdfs_checkbuttons[index].most_recent_selected:
                self.update_list_of_peaks(index)
                self.total_list_of_pdfs_checkbuttons[index].check_handled()
            elif self.total_list_of_pdfs_checkbuttons[index].most_recent_deselected:
                self.clear_active_peaks_list()
                self.total_list_of_pdfs_checkbuttons[index].check_handled()

    def clear_active_peaks_list(self):
        for entry in self.total_list_of_active_PDFs_peaks:
            entry.hide_entry()
        self.total_list_of_active_PDFs_peaks.clear()

    def update_list_of_peaks(self, Card_index):
        self.clear_active_peaks_list()

        the_card = self.Parent.PDF_Data_Containers[Card_index]
        the_data = the_card.get_list_of_data()
        the_activity_indices = the_card.get_list_of_active_indices()

        # Show current data
        for index in range(len(the_data)):
            self.total_list_of_active_PDFs_peaks.append(
                My_PDF_Entry_Interactive(self.mod_PDF_frame_scrolled2, the_data[index][1],
                                         the_data[index][0], the_data[index][2], 1+index, 1))

        for index in the_activity_indices:
            self.total_list_of_active_PDFs_peaks[index].set_is_active()

        # Add new rows for potentially adding rows to the PDF!
        for addition in range(4):
            self.total_list_of_active_PDFs_peaks.append(
                My_PDF_Entry_Interactive(self.mod_PDF_frame_scrolled2, "", 0, 0, 2+len(the_data)+addition, 1))

    def function_swap_pdf(self):
        pass

    def callback_OK_button(self):
        if self.selection_indication == 0: # New PDF inserted
            # Create tuples from entries and finally create a PDF-object to pass to parent, i.e. handler
            name = self.e_name.get_value()
            tup_list = []
            for entry in self.new_entries:
                if entry.get_2theta_value() > 0:
                    tup_list.append((entry.get_2theta_value(), entry.get_peak_name(), entry.get_Intensity_value()))
            index_list = list(range(len(tup_list)))
            new_data_container = PDF.PDF_Data(name, tup_list, index_list)
            self.Parent.add_new_pdf_data(new_data_container)

        elif self.selection_indication == 1: # Modified PDF card

            # find the pdf index to update.
            pdf_index = 0
            for index in range(len(self.total_list_of_pdfs_checkbuttons)):
                if self.total_list_of_pdfs_checkbuttons[index].is_active():
                    pdf_index = index
                    break

            # Create the new data from updates
            new_list_of_tuples = []
            new_list_of_activated_peaks = []
            for i in range(len(self.total_list_of_active_PDFs_peaks)):
                temp_name = self.total_list_of_active_PDFs_peaks[i].get_entry().get_peak_name()
                temp_2theta = self.total_list_of_active_PDFs_peaks[i].get_entry().get_2theta_value()
                temp_int = self.total_list_of_active_PDFs_peaks[i].get_entry().get_Intensity_value()
                if temp_2theta > 0: # Only include lines with nonzero 2theta
                    new_list_of_tuples.append((temp_2theta, temp_name, temp_int))
                    if self.total_list_of_active_PDFs_peaks[i].get_checkbutton().is_active():
                        new_list_of_activated_peaks.append(i)

            # make new pdf-card according to settings.
            # Delete the old and insert the new instead in the parent list of pdf:s!
            if new_list_of_tuples: # Check if anything in list.
                new_pdf_card = PDF.PDF_Data(self.Parent.PDF_Data_Containers[pdf_index].name,
                                            new_list_of_tuples, new_list_of_activated_peaks)

                self.Parent.PDF_Data_Containers.pop(pdf_index)
                self.Parent.PDF_Data_Containers.insert(pdf_index, new_pdf_card)
                self.Parent.Save_data_to_json_file()

            elif not new_list_of_tuples: # All data removed -> Remove PDF.
                self.Parent.PDF_Data_Containers.pop(pdf_index)
                self.Parent.Assert_active_indices_within_bounds()
                self.Parent.Save_data_to_json_file()


        elif self.selection_indication == 2: # Swap command
            for active_card_index in range(len(self.active_pdf_list_swap)):
                if self.active_pdf_list_swap[active_card_index].is_active(): # find pressed card to swap out
                    for other_card_index in range(len(self.total_pdf_list_swap)):
                        if self.total_pdf_list_swap[other_card_index].is_active(): # find (first) other card to swap in

                            # Update indices!
                            self.Parent.active_pdf[active_card_index] = other_card_index
                            self.Parent.Save_data_to_json_file()
                            self.Parent.Update_PDF_Buttons()
                            break


        self.popup_window.destroy()

    def callback_Cancel_button(self):
        self.popup_window.destroy()

    def callback_new_pdf_button(self):
        self.ungrid_selection_frames()
        self.new_PDF_frame.grid(row=1, column=0, sticky="EW")
        self.selection_indication = 0

    def callback_mod_pdf_button(self):
        self.ungrid_selection_frames()
        self.mod_PDF_frame.grid(row=1, column=0, sticky="EW")
        self.selection_indication = 1

    def callback_swap_pdf_button(self):
        self.ungrid_selection_frames()
        self.swap_PDF_frame.grid(row=1, column=0, sticky="EW")
        self.selection_indication = 2

    def ungrid_selection_frames(self):
        self.new_PDF_frame.grid_forget()
        self.mod_PDF_frame.grid_forget()
        self.swap_PDF_frame.grid_forget()